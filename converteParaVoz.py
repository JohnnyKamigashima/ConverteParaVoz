import boto3
import subprocess
import requests
import json
import os
import threading
import telebot
import sys
import re
import shutil
from pydub import AudioSegment

with open('../.openapi_credentials') as f:
    contents = f.read()

for line in contents.split('\n'):
    if line.startswith('api_key='):
        API_KEY = line[len('api_key='):]
    elif line.startswith('bot_token='):
        BOT_TOKEN = line[len('bot_token='):]

# Open api autentication files in ../.openapi_credentials
# api_key=
# api_secret=None

# Amazon Poly credentials in ../.aws/credentials
# [default]
# aws_access_key_id =
# aws_secret_access_key =
# region=us-east-1

# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
MODEL = 'gpt-3.5-turbo'

# Defining the bot's personality using adjectives
BOT_PERSONALITY = 'Escreva em português do Brasil, deixando o texto a seguir de forma mais clara.'

# Define response file
RESPONSE_BASEFILE = './responses/responseGPT'
CHAT_ID = "-1001899083389"
QUEUE_FILE = 'queue.txt'
AUDIO_EXTENSION = 'mp3'
OUTPUT_FILE = './responses/output'+'.'+AUDIO_EXTENSION


def merge_mp3_files(mp3_files, output_file):
    combined = AudioSegment.empty()
    for file in mp3_files:
        audio = AudioSegment.from_mp3(file)
        combined += audio
    combined.export(output_file, format=AUDIO_EXTENSION)

# Exemplo de uso
# mp3_files = ["file1.mp3", "file2.mp3", "file3.mp3"]
# output_file = "merged.mp3"
# merge_mp3_files(mp3_files, output_file)

def copy_file(source_file, destination_file):
    shutil.copyfile(source_file, destination_file)

def remover_quebras_duplas_e_espacos(string):
    # Remover quebras de linha duplicadas
    string = re.sub(r'\n+', '\n', string)

    # Remover espaços em branco duplicados
    string = re.sub(r' +', ' ', string)

    return string

def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # símbolos e pictogramas
                               u"\U0001F680-\U0001F6FF"  # transporte e símbolos de mapa
                               u"\U0001F1E0-\U0001F1FF"  # bandeiras de países
                               u"\U00002702-\U000027B0"  # símbolos diversos
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def polly_speak(response_file):
    # Crie uma instância do cliente da API Polly
    polly_client = boto3.client('polly')

    # Defina as configurações de voz e linguagem
    voice_id = 'Camila'
    language_code = 'pt-BR'
    engine = 'neural'

    # Defina o texto que será sintetizado em fala
    with open(response_file + '.txt', "r") as file:
        text = file.read()

    # Use o método synthesize_speech() da API Polly para sintetizar o texto em fala
    response = polly_client.synthesize_speech(
        OutputFormat=AUDIO_EXTENSION,
        Text=text,
        VoiceId=voice_id,
        LanguageCode=language_code,
        Engine=engine
    )

    # Salve o áudio sintetizado em um arquivo audio
    audio_file = response_file + '.'+AUDIO_EXTENSION
    with open(audio_file, 'wb') as f:
        f.write(response['AudioStream'].read())
        f.close()
    return audio_file
    # audio_send(CHAT_ID, audio_file)
    # command = MP3_PLAYER + " " + audio_file
    # subprocess.run(command, shell=True)

# 2a. Function that gets the response from OpenAI's chatbot
def open_ai(prompt):
    # Make the request to the OpenAI API
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': MODEL, 'messages': prompt, 'temperature': 0.01}
    )

    result = response.json()
    final_result = ''.join(choice['message'].get('content')
                           for choice in result['choices'])
    return final_result

def audio_send(chat_id, output_audio):
    bot = telebot.TeleBot(BOT_TOKEN)
    audio_file = open(output_audio, 'rb')
    bot.send_audio(chat_id, audio_file)

def limpar_linhas_vazias(texto):
    linhas = texto.split("\n")
    linhas_limpas = [linha for linha in linhas if linha.strip() != ""]
    texto_limpo = "\n".join(linhas_limpas)
    return texto_limpo

def telegram_bot_sendtext(bot_message, chat_id):
    data = {
        'chat_id': chat_id,
        'text': bot_message
    }
    response = requests.post(
        'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage',
        json=data
    )
    return response.json()

def main():
    with open(PROMPT_FILE, "r") as file:
        prompts = limpar_linhas_vazias(remove_emojis(file.read().strip()))
        contador_linhas = len(prompts.split('\n'))

    if contador_linhas == 1:
        telegram_bot_sendtext(prompts, CHAT_ID)

    if contador_linhas >= 1:
        promptList = prompts.split('\n')

        for index, prompt in enumerate(promptList):
            prompt = remover_quebras_duplas_e_espacos(prompt)
            string_formatada = "{:03d}".format(index)
            RESPONSE_FILE = RESPONSE_BASEFILE + str(string_formatada)

            if len(prompt) > 10:
                bot_response = open_ai(
                    [{'role': 'user', 'content': f'{BOT_PERSONALITY} {prompt}'}])

                bot_response = bot_response.replace('\n', '. ').strip()
                bot_response = bot_response.replace('..', '.')

                with open(RESPONSE_FILE + ".txt", "w") as file:
                    file.write(bot_response)

                polly_speak(RESPONSE_FILE)

                if index == 1:
                    copy_file(RESPONSE_FILE + '.' + AUDIO_EXTENSION, OUTPUT_FILE)
                else:
                    merge_mp3_files(
                        [OUTPUT_FILE, RESPONSE_FILE + '.' + AUDIO_EXTENSION], OUTPUT_FILE)

                os.remove(RESPONSE_FILE + ".txt")
                os.remove(RESPONSE_FILE + '.' + AUDIO_EXTENSION)

        audio_send(CHAT_ID, OUTPUT_FILE)
        os.remove(OUTPUT_FILE)
        bot_response = ""

    os.remove(PROMPT_FILE)

# Define Prompt file
while True:
    if len(sys.argv) < 2:
        print("Não foi fornecido argumento, usando lista queue.txt")
        with open(QUEUE_FILE, 'r') as file:
            PROMPT_FILE = file.readline().strip()
            print(PROMPT_FILE)
            lines = file.readlines()

        with open(QUEUE_FILE, 'w') as file:
            file.writelines(lines[1:])
        
        main()

    else:
        PROMPT_FILE = sys.argv[1]
        main()

    # Adicione aqui o restante do seu código que precisa ser executado repetidamente

    if len(lines) == 0:
        break
