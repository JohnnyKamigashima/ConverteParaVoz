import telebot


def audio_send(chat_id: str, output_audio: str, bot_token: str) -> None:
    """
    Send an audio file to a chat using a Telegram bot.

    Args:
        chat_id (int): The ID of the chat where the audio file will be sent.
        output_audio (str): The path to the audio file to be sent.

    Returns:
        None
    """
    bot = telebot.TeleBot(bot_token)
    with open(output_audio, 'rb') as audio_file:
        bot.send_audio(chat_id=chat_id, audio=audio_file, timeout=600)