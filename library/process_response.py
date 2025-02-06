from library.polly_speak import polly_speak
from library.write_response import write_response
from library.openai_speak import openai_speak

def process_response( api_key,response_file, bot_response):
    bot_response_byline = bot_response.split('. .')
    lista_arquivos_audio=[]
    lista_respostas=[]

    for index, response_line in enumerate(bot_response_byline):
        new_response_file = response_file + '_R_'+ str(index)
        write_response(new_response_file, response_line)
        lista_respostas.append(new_response_file+ '.txt')
        lista_arquivos_audio.append(openai_speak( api_key,new_response_file))
        # lista_arquivos_audio.append(polly_speak(new_response_file))

    return lista_arquivos_audio, lista_respostas