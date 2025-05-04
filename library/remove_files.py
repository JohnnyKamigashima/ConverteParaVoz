import os

from library.le_arquivo_texto import le_arquivo_texto
from library.telegram_bot import telegram_bot_sendtext


def remove_files(file_list) -> None:
    for file in file_list:
        if os.path.exists(file):
            os.remove(file)


def remove_all_files(chat_id, chat_token, lista_arquivos_audio, lista_respostas, mp3_file, ogg_file):
    print('Arquivos a serem removidos:\n')
    for fi in lista_arquivos_audio:
        print(fi)
    for fi in lista_respostas:
        telegram_bot_sendtext(le_arquivo_texto(fi), chat_id, chat_token)
        print(fi)
    print(mp3_file)
    print(ogg_file)
    remove_files(lista_arquivos_audio)
    remove_files(lista_respostas)
    remove_files([mp3_file, ogg_file])
