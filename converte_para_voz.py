"""  Converte arquivo texto para voz usando Amazon Polly
"""
import os
import sys
from library.copy_file import remove_files
from library.merge_mp3_files import convert_mp3_ogg, merge_mp3_files
from library.open_ai import query_openai, write_response
from library.splitString import divide_frases
from library.telegram_bot import audio_send, telegram_bot_sendtext
from library.text import \
    limpa_titulo, limpar_linhas_vazias, remove_emojis,\
        adicionar_quebras_de_linha, substituir_quebras_de_linha
from library.polly_speak import polly_speak

with open('../.openapi_credentials', encoding='utf-8') as f:
    contents = f.read()
API_KEY: str = ''
BOT_TOKEN: str = ''

for line in contents.split('\n'):
    if line.startswith('openai_api_key='):
        API_KEY: str = line[len('openai_api_key='):]
    elif line.startswith('bot_token='):
        BOT_TOKEN: str = line[len('bot_token='):]

# Open api autentication files in ../.openapi_credentials
# api_key=
# api_secret=None

# Amazon Poly credentials in ../.aws/credentials
# [default]
# aws_access_key_id =
# aws_secret_access_key =
# region=us-east-1

# Models: text-davinci-003,text-curie-001,text-babbage-001,text-ada-001
MODEL = 'gpt-4o-mini'

# Defining the bot's personality using adjectives
BOT_PERSONALITY = 'Resuma o texto para português do Brasil, \
    corrigindo com pontuação correta para uma melhor leitura, \
        detalhando cada idéia mencionada no texto de forma clara e simples que qualquer pessoa leiga consiga entender sem inventar novas idéias nem criar novos sentidos. \
            Se houver trechos de códigos, descreva a funcionalidade do código e o resultado gerado por ele e remova os trechos de código.\
                  Se houver cabeçalhos, indices e outros elementos que sejam irrelevantes para o entendimento do contexto, \
                    remova antes de traduzir. '

# Define response file
RESPONSE_BASE_FILE = './responses/responseGPT'
CHAT_ID = "-1001899083389"
QUEUE_FILE = 'queue.txt'
AUDIO_EXTENSION = 'mp3'
OUTPUT_FILE = './responses/output'+'.' + AUDIO_EXTENSION
OGG_OUTPUT_FILE = './responses/output'+'.' + 'ogg'
AUDIO_OUTPUT_PATH = './responses/'
TEXTO_INDESEJADO: list[str] = [
    'Reescreva em português do Brasil, corrigindo com pontuação correta para uma melhor leitura',
    'Reescrevendo com pontuação correta:',
    'Reescrevendo em português do Brasil, com a pontuação correta para uma melhor leitura:',
    BOT_PERSONALITY
    ]

def main(prompt_from_file, chat_id, chat_token, api_key):
    """
    This is the main function of the program.
    It reads prompts from a file and sends them to a Telegram chat.
    """
    # rest of the code...
    with open(prompt_from_file, "r", encoding="utf-8") as file:
        prompts = limpar_linhas_vazias(remove_emojis(file.read().strip()))
        prompts = adicionar_quebras_de_linha(substituir_quebras_de_linha(prompts,200),400)
        contador_linhas = len(prompts.split('\n\n'))
        lista_arquivos_audio = []
        lista_respostas = []

    if contador_linhas == 1:
        telegram_bot_sendtext(prompts, chat_id,chat_token)

    if contador_linhas >= 1:
        prompt_list: list[str] =  list(filter(None,divide_frases(prompts)))
        titulo_texto: str = ''
        mp3_file: str = ''
        ogg_file: str = ''

        titulo_texto, mp3_file, ogg_file = \
            generate_reponse(api_key, lista_arquivos_audio, lista_respostas, prompt_list)

        print(f'Arquivos da lista de arquivos de audio:\n {lista_arquivos_audio}:\n')
        merge_mp3_files(lista_arquivos_audio, mp3_file)
        convert_mp3_ogg(mp3_file, ogg_file)
        telegram_bot_sendtext(titulo_texto, chat_id, chat_token)
        audio_send(chat_id, ogg_file, chat_token )

        print('Arquivoa a serem removidos:\n')
        for fi in lista_arquivos_audio:
            print(fi)
        for fi in lista_respostas:
            print(fi)
        print(mp3_file)
        print(ogg_file)

        remove_files(lista_arquivos_audio)
        remove_files(lista_respostas)
        remove_files([mp3_file, ogg_file])

def generate_reponse(api_key, lista_arquivos_audio, lista_respostas, prompt_list):
    for index, prompt in enumerate(prompt_list):
        string_formatada: str = f"{index:03d}"
        response_file: str = RESPONSE_BASE_FILE + str(string_formatada)

        if len(prompt) > 10:
            if index == 0:
                titulo_texto: str = limpa_titulo(prompt, 30)
                mp3_file = AUDIO_OUTPUT_PATH + titulo_texto + '.' + AUDIO_EXTENSION
                ogg_file = AUDIO_OUTPUT_PATH + titulo_texto + '.' + 'ogg'
            bot_response: str = \
                    query_openai(prompt, MODEL, api_key, BOT_PERSONALITY, TEXTO_INDESEJADO)

            process_response(lista_arquivos_audio, lista_respostas, response_file, bot_response)
    return titulo_texto,mp3_file,ogg_file

def process_response(lista_arquivos_audio, lista_respostas, response_file, bot_response):
    bot_response_byline = bot_response.split('. .')

    for index, response_line in enumerate(bot_response_byline):
        new_response_file = response_file + '_R_'+ str(index)
        write_response(new_response_file, response_line)
        lista_respostas.append(new_response_file+ '.txt')
        lista_arquivos_audio.append(polly_speak(new_response_file))

while True:
    # Get all .txt files in the current directory
    txt_files = [f for f in os.listdir() if f.endswith('.txt')]

    if len(txt_files) == 0:
        print("No .txt files found in the current directory. Exiting the program.")
        break

    for prompt_file in txt_files:
        if prompt_file != '' and os.path.exists(prompt_file):
            main(prompt_file, CHAT_ID, BOT_TOKEN, API_KEY)
            os.remove(prompt_file)
            

