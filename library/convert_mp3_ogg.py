from pydub import AudioSegment


def convert_mp3_ogg(input_file:str ,output_file:str):
    """
    Converts an mp3 file to ogg format.

    Args:
        input_file (str): The path to the input mp3 file.
        output_file (str): The path to the output ogg file.

    Returns:
        None
    """
    sound = AudioSegment.from_file(input_file, format="mp3")
    sound.export(output_file, format="ogg")