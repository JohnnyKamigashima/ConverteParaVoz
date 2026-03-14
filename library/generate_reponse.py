from library.variables import AUDIO_EXTENSION, AUDIO_OUTPUT_PATH, BOT_PERSONALITY, MODEL, RESPONSE_BASE_FILE, TEXTO_INDESEJADO
from library.limpa_titulo import limpa_titulo
from library.query_openai import query_openai
from library.process_response import process_response


def generate_response(api_key: str, prompt_list: list[str]) -> tuple[str, str, str, list[str], list[str]]:
    """Gera respostas em texto/audio para cada prompt e retorna os artefatos finais."""
    lista_arquivos_audio_final: list[str] = []
    lista_resposta_final: list[str] = []
    mp3_file: str = ''
    ogg_file: str = ''
    titulo_texto: str = 'sem_titulo'
    ogg_extension: str = 'ogg'
    titulo_comprimento: int = 125

    for index, prompt in enumerate(prompt_list):
        string_formatada: str = f"{index:03d}"
        response_file: str = RESPONSE_BASE_FILE + str(string_formatada)

        if len(prompt) > 10:
            if index == 0:
                titulo_texto: str = limpa_titulo(prompt, titulo_comprimento)
                mp3_file = AUDIO_OUTPUT_PATH + titulo_texto + '.' + AUDIO_EXTENSION
                ogg_file = AUDIO_OUTPUT_PATH + titulo_texto + '.' + ogg_extension
            bot_response: str = query_openai(prompt, MODEL, api_key, BOT_PERSONALITY, TEXTO_INDESEJADO)
            lista_arquivos_audio, lista_respostas = process_response(api_key, response_file, bot_response)
            lista_arquivos_audio_final.extend(lista_arquivos_audio)
            lista_resposta_final.extend(lista_respostas)

    return titulo_texto, mp3_file, ogg_file, lista_arquivos_audio_final, lista_resposta_final


def generate_reponse(api_key: str, prompt_list: list[str]) -> tuple[str, str, str, list[str], list[str]]:
    """Alias de compatibilidade para chamadas legadas."""
    return generate_response(api_key, prompt_list)