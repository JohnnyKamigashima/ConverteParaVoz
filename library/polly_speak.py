""" Fonctions to work with Amazon Polly
"""

import boto3

def polly_speak(
    response_file,
    extension = '.txt',
    voice_id = 'Camila',
    language_code = 'pt-BR',
    output_format = 'mp3'
    ):

    """
    Generates a speech audio file using the Amazon Polly API.

    Parameters:
        response_file (str): The path to the file containing the text to be synthesized.

    Returns:
        str: The path to the generated speech audio file.
    """

    # Create an instance of the Polly API client
    polly_client = boto3.client('polly')

    # Set voice and language settings
    engine = 'neural'

    # Read the text to be synthesized from the file
    with open(response_file + extension, "r", encoding="utf-8") as file:
        text = file.read()

    # Synthesize the text into speech using the Polly API's synthesize_speech() method
    response = polly_client.synthesize_speech(
        OutputFormat=output_format,
        Text=text,
        VoiceId=voice_id,
        LanguageCode=language_code,
        Engine=engine
    )

    # Save the synthesized audio to a file
    audio_file = response_file + '.' + output_format
    with open(audio_file, 'wb') as file:
        file.write(response['AudioStream'].read())

    return audio_file
