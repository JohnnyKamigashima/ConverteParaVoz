import os
from collections.abc import Iterable

from library.le_arquivo_texto import le_arquivo_texto
from library.telegram_bot import telegram_bot_sendtext


def remove_files(file_list: Iterable[str]) -> None:
    """Remove todos os arquivos existentes recebidos em uma colecao."""
    for file_path in file_list:
        if os.path.exists(file_path):
            os.remove(file_path)


def remove_all_files(
    chat_id: str,
    chat_token: str,
    lista_arquivos_audio: list[str],
    lista_respostas: list[str],
    mp3_file: str,
    ogg_file: str,
) -> None:
    """Envia respostas em texto para o Telegram e remove arquivos temporarios."""
    print("Arquivos a serem removidos:\n")
    for audio_file in lista_arquivos_audio:
        print(audio_file)

    for response_file in lista_respostas:
        telegram_bot_sendtext(le_arquivo_texto(response_file), chat_id, chat_token)
        print(response_file)

    print(mp3_file)
    print(ogg_file)
    remove_files(lista_arquivos_audio)
    remove_files(lista_respostas)
    remove_files([mp3_file, ogg_file])
