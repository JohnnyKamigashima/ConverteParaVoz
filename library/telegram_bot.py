"""Funções de Telegram Bot
"""
from typing import Any

import requests


def telegram_bot_sendtext(bot_message: str, chat_id: str, bot_token: str) -> dict[str, Any]:
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
    api_url: str = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    response = requests.post(
        api_url,
        json=data,
        timeout=60000
    )
    return response.json()
