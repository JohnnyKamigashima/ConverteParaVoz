import telebot


def audio_send(chat_id, output_audio, bot_token):
    """
    Send an audio file to a chat using a Telegram bot.

    Args:
        chat_id (int): The ID of the chat where the audio file will be sent.
        output_audio (str): The path to the audio file to be sent.

    Returns:
        None
    """
    bot = telebot.TeleBot(bot_token)
    audio_file = open(output_audio, 'rb')
    bot.send_audio(chat_id = chat_id, audio = audio_file, timeout=600)