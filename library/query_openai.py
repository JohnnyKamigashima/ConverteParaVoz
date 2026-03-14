from library.open_ai import open_ai
from collections.abc import Sequence


def query_openai(
    prompt: str,
    model: str,
    api_key_value: str,
    bot_personality_value: str,
    texto_indesejado: Sequence[str],
) -> str:
    """
    Queries the OpenAI API with a given prompt and returns the bot's response.

    Args:
        prompt (str): The prompt to send to the OpenAI API.
        model (str): The ID of the OpenAI model to use.
        api_key_value (str): The API key for the OpenAI API.
        bot_personality_value (str): The personality of the bot to use in the response.
        texto_indesejado (list[str]): The list of words that the bot should not use in the response.

    Returns:
        str: The bot's response to the given prompt.
    """
    prompt = prompt.strip()
    print("\nPROMPT => " + prompt)
    bot_response: str = open_ai(
        bot_personality_value,
        prompt,
        api_key_value,
        model
    )
    bot_response = bot_response.replace('\n', '. ').strip()
    bot_response = bot_response.replace('..', '.')

    for unwanted_text in texto_indesejado:
        if unwanted_text in bot_response:
            bot_response = bot_response.replace(unwanted_text, '')
    return bot_response