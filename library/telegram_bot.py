"""Funções de Telegram Bot
"""
import telebot
import requests

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
    bot.send_audio(chat_id = chat_id, audio = audio_file, timeout=120)

def telegram_bot_sendtext(bot_message, chat_id, bot_token):
    """
    Sends a text message to a Telegram bot.

    Args:
        bot_message (str): The message to be sent to the bot.
        chat_id (int): The ID of the chat where the message will be sent.

    Returns:
        dict: The JSON response from the Telegram API.
    """
    data = {
        'chat_id': chat_id,
        'text': bot_message
    }
    response = requests.post(
        'https://api.telegram.org/bot' + bot_token + '/sendMessage',
        json=data,
        timeout=60000
    )
    return response.json()
