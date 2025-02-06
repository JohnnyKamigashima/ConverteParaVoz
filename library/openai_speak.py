""" Functions to work with OpenAi
"""

from openai import OpenAI

def openai_speak(
    token,
    response_file,
    extension = '.txt',
    voice_id = 'nova',
    model = 'tts-1-hd',
    output_format = 'mp3',
    ):

    client = OpenAI(api_key=token)
    with open(response_file + extension, "r", encoding="utf-8") as file:
        text = file.read()

    response = client.audio.speech.create(
        model=model,
        voice=voice_id,
        input=text,
    )

    # Save the synthesized audio to a file
    audio_file = response_file + '.' + output_format
    response.stream_to_file(audio_file)

    return audio_file
