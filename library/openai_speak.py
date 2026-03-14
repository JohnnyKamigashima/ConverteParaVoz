""" Functions to work with OpenAi
"""

from openai import OpenAI


def openai_speak(
    token: str,
    response_file: str,
    extension: str = '.txt',
    voice_id: str = 'nova',
    model: str = 'tts-1',
    output_format: str = 'mp3',
) -> str:

    client = OpenAI(api_key=token)
    with open(response_file + extension, "r", encoding="utf-8") as file:
        text: str = file.read()

    response = client.audio.speech.create(
        model=model,
        voice=voice_id,
        input=text,
    )

    audio_file: str = response_file + '.' + output_format
    response.stream_to_file(audio_file)

    return audio_file
