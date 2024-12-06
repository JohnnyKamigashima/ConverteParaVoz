from library.open_ai import open_ai


def query_openai(prompt, model, api_key_value, bot_personality_value, texto_indesejado) -> str:
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

    for i in texto_indesejado:
        if i in bot_response:
            bot_response = bot_response.replace(i, '')
    return bot_response