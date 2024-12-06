"""Funções de Telegram Bot
"""
import requests

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
