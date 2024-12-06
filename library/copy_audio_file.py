from library.copy_file import copy_file


import os


def copy_audio_file(response_file, output_file, audio_extension):
    """
    Copies the audio file with the specified extension from the response_file to the output_file.

    Args:
    response_file (str): The path to the response file.
    output_file (str): The path to the output file.
    audio_extension (str): The extension of the audio file.

    Returns:
    None
    """
    if os.path.exists(response_file + '.' + audio_extension):
        copy_file(response_file + '.' + audio_extension, output_file)