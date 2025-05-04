import os
from library.generate_reponse import generate_reponse
from library.adicionar_quebras_de_linha import adicionar_quebras_de_linha
from library.audio_send import audio_send
from library.convert_mp3_ogg import convert_mp3_ogg
from library.remove_emojis import remove_emojis
from library.remove_files import remove_all_files
from library.merge_mp3_files import merge_mp3_files
from library.substituir_quebras_de_linha import substituir_quebras_de_linha
from library.splitString import divide_frases
from library.telegram_bot import telegram_bot_sendtext
from library.text import \
    limpar_linhas_vazias
from library.variables import API_KEY, BOT_TOKEN, CHAT_ID

def main(prompt_from_file, chat_id, chat_token, api_key):
    with open(prompt_from_file, "r", encoding="utf-8") as file:
        prompts = limpar_linhas_vazias(remove_emojis(file.read().strip()))
        prompts = adicionar_quebras_de_linha(substituir_quebras_de_linha(prompts,200),400)
        contador_linhas = len(prompts.split('.\n\n'))

    if contador_linhas >= 1:
        prompt_list: list[str] =  list(filter(None,divide_frases(prompts)))

        titulo_texto, mp3_file, ogg_file, lista_arquivos_audio, lista_respostas = \
            generate_reponse(api_key, prompt_list)

        merge_mp3_files(lista_arquivos_audio, mp3_file, "mp3")
        convert_mp3_ogg(mp3_file, ogg_file)
        telegram_bot_sendtext(titulo_texto, chat_id, chat_token)
        audio_send(chat_id, ogg_file, chat_token )

        remove_all_files(chat_id, chat_token, lista_arquivos_audio, lista_respostas, mp3_file, ogg_file)


while True:
    txt_files = sorted([f for f in os.listdir() if f.endswith('.txt')])

    if len(txt_files) == 0:
        print("No .txt files found in the current directory. Exiting the program.")
        break

    for prompt_file in txt_files:
        if prompt_file != '' and os.path.exists(prompt_file):
            main(prompt_file, CHAT_ID, BOT_TOKEN, API_KEY)
            os.remove(prompt_file)

