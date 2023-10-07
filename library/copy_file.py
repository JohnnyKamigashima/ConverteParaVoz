"""Copia arquivos
"""
import os
import shutil

from library.merge_mp3_files import convert_mp3_ogg
from library.telegram_bot import audio_send
def copy_file(source_file, destination_file):
    """
    Copy a file from the source path to the destination path.

    Args:
        source_file (str): The path of the source file to be copied.
        destination_file (str): The path where the source file should be copied to.

    Returns:
        None
    """
    shutil.copyfile(source_file, destination_file)

def remove_files(file_list) -> None:
    """
    Removes a list of files from the file system.

    Args:
        file_list (list): A list of file paths to be removed.

    Returns:
        None
    """
    for file in file_list:
        if os.path.exists(file):
            os.remove(file)

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

