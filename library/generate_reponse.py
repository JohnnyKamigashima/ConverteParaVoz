from library.variables import AUDIO_EXTENSION, AUDIO_OUTPUT_PATH, BOT_PERSONALITY, MODEL, RESPONSE_BASE_FILE, TEXTO_INDESEJADO
from library.limpa_titulo import limpa_titulo
from library.query_openai import query_openai
from library.process_response import process_response

def generate_reponse(api_key, prompt_list):
    lista_arquivos_audio_final = []
    lista_resposta_final = []
    mp3_file = ''
    ogg_file = ''
    ogg_extension = 'ogg'
    titulo_comprimento = 125

    for index, prompt in enumerate(prompt_list):
        string_formatada: str = f"{index:03d}"
        response_file: str = RESPONSE_BASE_FILE + str(string_formatada)

        if len(prompt) > 10:
            if index == 0:
                titulo_texto: str = limpa_titulo(prompt, titulo_comprimento)
                mp3_file = AUDIO_OUTPUT_PATH + titulo_texto + '.' + AUDIO_EXTENSION
                ogg_file = AUDIO_OUTPUT_PATH + titulo_texto + '.' + ogg_extension
            bot_response: str = \
                    query_openai(prompt, MODEL, api_key, BOT_PERSONALITY, TEXTO_INDESEJADO)

            lista_arquivos_audio, lista_respostas = process_response(api_key,response_file, bot_response)
            lista_arquivos_audio_final.extend(lista_arquivos_audio)
            lista_resposta_final.extend(lista_respostas)

    return titulo_texto,mp3_file,ogg_file, lista_arquivos_audio_final, lista_resposta_final