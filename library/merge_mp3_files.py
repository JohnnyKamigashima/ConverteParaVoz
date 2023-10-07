""" Concatena mp3 files
"""
from pydub import AudioSegment
from pydub.utils import make_chunks
    # Exemplo de uso
    # mp3_files = ["file1.mp3", "file2.mp3", "file3.mp3"]
    # output_file = "merged.mp3"
    # merge_mp3_files(mp3_files, output_file)
def merge_mp3_files(mp3_files, output_file, audio_extension="mp3"):
    """
    Merges multiple MP3 files into a single output file.

    Parameters:
        mp3_files (List[str]): A list of paths to the MP3 files to be merged.
        output_file (str): The path to the output file.

    Returns:
        None
    """
    combined = AudioSegment.empty()

    for file in mp3_files:
        audio = AudioSegment.from_mp3(file)
        combined += audio

    combined.export(output_file, format=audio_extension, bitrate="128k")

def normalize_audio(file_name):
    """
    Normalize the audio file by loading it, dividing it into 1-second segments,
    calculating the RMS value of each segment, and normalizing the volume. 
    Then, join the normalized segments and export the normalized audio to a new MP3 file.

    Args:
        file_name (str): The name of the MP3 file to be normalized.

    Returns:
        None
    """
    # Carrega o arquivo MP3
    audio = AudioSegment.from_file(file_name, format="mp3")

    # Divide o áudio em segmentos de 1 segundo
    chunks = make_chunks(audio, 1000)

    # Calcula o valor RMS de cada segmento e normaliza o volume
    normalized_audio = AudioSegment.empty()
    for chunk in chunks:
        rms = chunk.rms
        normalized_chunk = chunk - (rms - 100)
        normalized_audio += normalized_chunk

    # Exporta o áudio normalizado para um novo arquivo MP3
    normalized_file_name = file_name.replace(".mp3", "_normalized.mp3")
    normalized_audio.export(normalized_file_name, format="mp3", bitrate="320k")

    print("Áudio normalizado salvo como:", normalized_file_name)
    return normalized_file_name

def convert_mp3_ogg(input_file):
    """
    Converts an mp3 file to ogg format.

    Args:
        input_file (str): The path to the input mp3 file.

    Returns:
        None
    """
    sound = AudioSegment.from_file(input_file, format="mp3")
    sound.export(input_file, format="ogg")

def merge_audio(response_file, output_file, audio_extension):
    """
    Merges an audio file with another audio file and saves the result to the output file.

    Args:
        response_file (str): The path to the audio file to be merged.
        output_file (str): The path to the output file.
        audio_extension (str): The extension of the audio file.

    Returns:
        None
    """
    if os.path.exists(output_file):
        merge_mp3_files(
            [output_file, response_file + '.' + audio_extension], output_file)

import os

