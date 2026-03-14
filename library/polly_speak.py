""" Functions to work with Amazon Polly
"""

import boto3


def polly_speak(
    response_file: str,
    extension: str = '.txt',
    voice_id: str = 'Camila',
    language_code: str = 'pt-BR',
    output_format: str = 'mp3',
) -> str:

    """
    Generates a speech audio file using the Amazon Polly API.

    Parameters:
        response_file (str): The path to the file containing the text to be synthesized.

    Returns:
        str: The path to the generated speech audio file.
    """

    polly_client = boto3.client('polly')

    engine: str = 'neural'

    with open(response_file + extension, "r", encoding="utf-8") as file:
        text: str = file.read()

    response = polly_client.synthesize_speech(
        OutputFormat=output_format,
        Text=  text  ,
        VoiceId=voice_id,
        LanguageCode=language_code,
        Engine=engine
    )

    audio_file: str = response_file + '.' + output_format
    with open(audio_file, 'wb') as file:
        file.write(response['AudioStream'].read())

    return audio_file
