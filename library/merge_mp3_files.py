""" Concatena mp3 files
"""
from collections.abc import Sequence

from pydub import AudioSegment


def merge_mp3_files(mp3_files: Sequence[str], output_file: str, audio_extension: str = "mp3") -> str:
    """
    Merges multiple MP3 files into a single output file.

    Parameters:
        mp3_files (List[str]): A list of paths to the MP3 files to be merged.
        output_file (str): The path to the output file.

    Returns:
        None
    """
    combined: AudioSegment = AudioSegment.empty()
    print(f'mp3_files {mp3_files}')

    for file in mp3_files:
        audio = AudioSegment.from_mp3(file)
        combined += audio

    combined.export(output_file, format=audio_extension, bitrate="320k")
    return output_file

