from pyht import Client
from pyht.client import TTSOptions
import os

client = Client(
    user_id="YvWU5edrpTSEHlkHJRIOplYqFS12",
    api_key="d1147fc278074a06a69211ca2ec268d1",
)

def play_ht(response_file,extension = '.txt',
    output_format = 'mp3',):
    with open(response_file + ".txt", "r", encoding="utf-8") as file:
        text = file.read()
        options = TTSOptions(voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json")
        for chunk in client.tts(text, options):
            audio_file = response_file + '.' + output_format
            with open(audio_file, 'wb') as file:
                file.write(chunk)

            return audio_file