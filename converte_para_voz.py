"""  Converte arquivo texto para voz usando Amazon Polly
"""
import os
import sys
from library.copy_file import copy_audio_file, remove_files, send_and_remove
from library.merge_mp3_files import merge_audio
from library.open_ai import query_openai, write_response
from library.telegram_bot import telegram_bot_sendtext
from library.text import limpar_linhas_vazias, remove_emojis, adicionar_quebras_de_linha, substituir_quebras_de_linha
from library.polly_speak import polly_speak

with open('../.openapi_credentials', encoding='utf-8') as f:
    contents = f.read()

for line in contents.split('\n'):
    if line.startswith('api_key='):
        api_key = line[len('api_key='):]
    elif line.startswith('bot_token='):
        bot_token = line[len('bot_token='):]

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
bot_personality = 'Reescreva em português do Brasil, corrigindo com pontuação correta para uma melhor leitura.'

# Define response file
RESPONSE_BASE_FILE = './responses/responseGPT'
CHAT_ID = "-1001899083389"
QUEUE_FILE = 'queue.txt'
AUDIO_EXTENSION = 'mp3'
OUTPUT_FILE = './responses/output'+'.' + AUDIO_EXTENSION
OGG_OUTPUT_FILE = './responses/output'+'.' + 'ogg'

def main(prompt_file, chat_id, chat_token):
    """
    This is the main function of the program.
    It reads prompts from a file and sends them to a Telegram chat.
    """
    # rest of the code...
    with open(prompt_file, "r", encoding="utf-8") as file:
        prompts = limpar_linhas_vazias(remove_emojis(file.read().strip()))
        prompts = adicionar_quebras_de_linha(substituir_quebras_de_linha(prompts,200),400)
        contador_linhas = len(prompts.split('\n'))

    if contador_linhas == 1:
        telegram_bot_sendtext(prompts, chat_id,chat_token)

    if contador_linhas >= 1:
        prompt_list = prompts.split('\n')

        for index, prompt in enumerate(prompt_list):
            string_formatada = f"{index:03d}"
            response_file = RESPONSE_BASE_FILE + str(string_formatada)

            if len(prompt) > 10:
                bot_response = query_openai(prompt, MODEL, api_key, bot_personality)
                bot_response = bot_response.replace('\n', '. ').strip()
                bot_response = bot_response.replace('..', '.')
                print('\nRESPONSE => ' + bot_response)

                write_response(response_file, bot_response)
                polly_speak(response_file)

                if index == 0:
                    copy_audio_file(response_file, OUTPUT_FILE, AUDIO_EXTENSION)
                else:
                    merge_audio(response_file, OUTPUT_FILE, AUDIO_EXTENSION)

                remove_files(response_file, AUDIO_EXTENSION)

        send_and_remove(OUTPUT_FILE, OGG_OUTPUT_FILE, chat_token, chat_id)

        bot_response = ""

while True:
    if len(sys.argv) < 2:
        print("Não foi fornecido argumento, usando lista queue.txt")
        with open(QUEUE_FILE, 'r', encoding='utf-8') as p_file:
            prompt_file = p_file.readline().strip()
            print(prompt_file)

        if prompt_file != '' and os.path.exists(prompt_file):
            main(prompt_file, CHAT_ID, bot_token)
            os.remove(prompt_file)

        with open(QUEUE_FILE, 'w',encoding='utf-8') as p_file:
            lines = p_file.readlines()
            p_file.writelines(lines[1:])

            if len(lines) == 0:
                break

    else:
        prompt_file = sys.argv[1]
        main(prompt_file, CHAT_ID, bot_token)
