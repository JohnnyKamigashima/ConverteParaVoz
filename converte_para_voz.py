"""  Converte arquivo texto para voz usando Amazon Polly
"""
import sys
import os
from library.text import limpar_linhas_vazias, remove_emojis, remover_quebras_duplas_e_espacos
from library.telegram_bot import telegram_bot_sendtext, audio_send
from library.open_ai import open_ai
from library.polly_speak import polly_speak
from library.merge_mp3_files import merge_mp3_files, normalize_audio
from library.copy_file import copy_file

with open('../.openapi_credentials', encoding='utf-8') as f:
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
BOT_PERSONALITY = 'Reescreva em português do Brasil, corrigindo com pontuação correta para uma melhor leitura.'

# Define response file
RESPONSE_BASE_FILE = './responses/responseGPT'
CHAT_ID = "-1001899083389"
QUEUE_FILE = 'queue.txt'
AUDIO_EXTENSION = 'mp3'
OUTPUT_FILE = './responses/output'+'.' + AUDIO_EXTENSION

def main():
    """
    This is the main function of the program.
    It reads prompts from a file and sends them to a Telegram chat.
    """
    # rest of the code...
    with open(PROMPT_FILE, "r", encoding="utf-8") as file:
        prompts = limpar_linhas_vazias(remove_emojis(file.read().strip()))
        contador_linhas = len(prompts.split('\n'))

    if contador_linhas == 1:
        telegram_bot_sendtext(prompts, CHAT_ID,BOT_TOKEN)

    if contador_linhas >= 1:
        prompt_list = prompts.split('\n')

        for index, prompt in enumerate(prompt_list):
            prompt = remover_quebras_duplas_e_espacos(prompt)
            string_formatada = f"{index:03d}"
            response_file = RESPONSE_BASE_FILE + str(string_formatada)

            if len(prompt) > 10:
                bot_response = open_ai(
                                        [{
                                            'role': 'user',
                                            'content': f'{BOT_PERSONALITY} {prompt}'
                                            }],
                                        API_KEY,
                                        MODEL,
                                        base_url='https://api.openai.com'
                                        )

                bot_response = bot_response.replace('\n', '. ').strip()
                bot_response = bot_response.replace('..', '.')

                with open(response_file + '.txt', "w", encoding="utf-8") as file:
                    file.write(bot_response)

                polly_speak(response_file)

                if index == 0:
                    copy_file(response_file + '.' + AUDIO_EXTENSION, OUTPUT_FILE)
                else:
                    merge_mp3_files(
                        [OUTPUT_FILE, response_file + '.' + AUDIO_EXTENSION], OUTPUT_FILE)

                os.remove(response_file + ".txt")
                os.remove(response_file + '.' + AUDIO_EXTENSION)

        normalized_file = normalize_audio(OUTPUT_FILE)
        audio_send(CHAT_ID, normalized_file, BOT_TOKEN)
        os.remove(OUTPUT_FILE)
        os.remove(normalized_file)
        bot_response = ""

    os.remove(PROMPT_FILE)

# Define Prompt file
while True:
    if len(sys.argv) < 2:
        print("Não foi fornecido argumento, usando lista queue.txt")
        with open(QUEUE_FILE, 'r', encoding='utf-8') as p_file:
            PROMPT_FILE = p_file.readline().strip()
            print(PROMPT_FILE)
            lines = p_file.readlines()

        with open(QUEUE_FILE, 'w',encoding='utf-8') as p_file:
            p_file.writelines(lines[1:])
        if PROMPT_FILE != '':
            main()

    else:
        PROMPT_FILE = sys.argv[1]
        main()

    # Adicione aqui o restante do seu código que precisa ser executado repetidamente

    if len(lines) == 0:
        break
