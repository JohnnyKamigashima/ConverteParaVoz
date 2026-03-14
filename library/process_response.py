from library.write_response import write_response
from library.openai_speak import openai_speak


def process_response(api_key: str, response_file: str, bot_response: str) -> tuple[list[str], list[str]]:
    """Gera arquivos de texto/audio para cada trecho da resposta do bot."""
    bot_response_byline: list[str] = bot_response.split('. .')
    lista_arquivos_audio: list[str] = []
    lista_respostas: list[str] = []

    for index, response_line in enumerate(bot_response_byline):
        new_response_file: str = response_file + '_R_' + str(index)
        texto_gerado: str = write_response(new_response_file, response_line)
        lista_respostas.append(texto_gerado)
        lista_arquivos_audio.append(openai_speak(api_key, new_response_file))

    return lista_arquivos_audio, lista_respostas