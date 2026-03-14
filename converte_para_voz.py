"""Ponto de entrada para converter textos em audio e enviar ao Telegram."""

from __future__ import annotations

from pathlib import Path

from library.adicionar_quebras_de_linha import adicionar_quebras_de_linha
from library.audio_send import audio_send
from library.convert_mp3_ogg import convert_mp3_ogg
from library.generate_reponse import generate_response
from library.merge_mp3_files import merge_mp3_files
from library.remove_emojis import remove_emojis
from library.remove_files import remove_all_files
from library.splitString import divide_frases
from library.substituir_quebras_de_linha import substituir_quebras_de_linha
from library.telegram_bot import telegram_bot_sendtext
from library.text import limpar_linhas_vazias
from library.variables import API_KEY, BOT_TOKEN, CHAT_ID

TXT_EXTENSION: str = ".txt"
MAX_LINE_WIDTH: int = 200
MAX_BREAK_WIDTH: int = 400


def list_prompt_files() -> list[Path]:
    """Retorna todos os arquivos .txt no diretorio atual, ordenados por nome."""
    return sorted(path for path in Path.cwd().iterdir() if path.suffix == TXT_EXTENSION)


def process_prompt_file(prompt_file: Path, chat_id: str, chat_token: str, api_key: str) -> None:
    """Processa um arquivo de prompt, gera audio e faz o envio para o Telegram."""
    prompt_text: str = prompt_file.read_text(encoding="utf-8").strip()
    sanitized_text: str = limpar_linhas_vazias(remove_emojis(prompt_text))
    normalized_text: str = substituir_quebras_de_linha(sanitized_text, MAX_LINE_WIDTH)
    prompts: str = adicionar_quebras_de_linha(normalized_text, MAX_BREAK_WIDTH)

    if not prompts.strip():
        return

    prompt_list: list[str] = [phrase for phrase in divide_frases(prompts) if phrase]
    if not prompt_list:
        return

    (
        title_text,
        mp3_file,
        ogg_file,
        audio_files,
        response_files,
    ) = generate_response(api_key, prompt_list)

    merge_mp3_files(audio_files, mp3_file, "mp3")
    convert_mp3_ogg(mp3_file, ogg_file)
    telegram_bot_sendtext(title_text, chat_id, chat_token)
    audio_send(chat_id, ogg_file, chat_token)
    remove_all_files(chat_id, chat_token, audio_files, response_files, mp3_file, ogg_file)


def main() -> None:
    """Loop principal de leitura e processamento de arquivos de texto."""
    while True:
        txt_files: list[Path] = list_prompt_files()
        if not txt_files:
            print("No .txt files found in the current directory. Exiting the program.")
            break

        for prompt_file in txt_files:
            if prompt_file.exists():
                process_prompt_file(prompt_file, CHAT_ID, BOT_TOKEN, API_KEY)
                prompt_file.unlink()


if __name__ == "__main__":
    main()

