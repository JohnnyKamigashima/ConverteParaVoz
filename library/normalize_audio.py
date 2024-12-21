from pydub import AudioSegment
from pydub.utils import make_chunks


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