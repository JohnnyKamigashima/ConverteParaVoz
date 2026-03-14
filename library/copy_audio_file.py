from library.copy_file import copy_file


import os


def copy_audio_file(response_file: str, output_file: str, audio_extension: str) -> None:
    """
    Copies the audio file with the specified extension from the response_file to the output_file.

    Args:
    response_file (str): The path to the response file.
    output_file (str): The path to the output file.
    audio_extension (str): The extension of the audio file.

    Returns:
    None
    """
    source_audio_file: str = f"{response_file}.{audio_extension}"
    if os.path.exists(source_audio_file):
        copy_file(source_audio_file, output_file)