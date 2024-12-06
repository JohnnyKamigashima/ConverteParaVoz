""" Concatena mp3 files
"""
from pydub import AudioSegment
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
    print(f'mp3_files {mp3_files}')

    for file in mp3_files:
        audio = AudioSegment.from_mp3(file)
        combined += audio

    combined.export(output_file, format=audio_extension, bitrate="320k")

