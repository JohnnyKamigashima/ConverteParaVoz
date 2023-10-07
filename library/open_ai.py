""" Funções para usar OpenAi Api
"""

import requests
from requests.exceptions import HTTPError

def open_ai(prompt, api_key, model, base_url, max_retries=3):
    """
    Improved version of the open_ai function.

    Args:
        prompt (dict): The prompt for the OpenAI API.
        api_key (str): The API key for authentication.
        model (str): The model to use for the API request.
        base_url (str): The base URL for the API request.
        max_retries (int): The maximum number of retries in case of exception.

    Returns:
        str: The final result from the API response.
    """

    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(
                f'{base_url}/v1/chat/completions',
                headers={'Authorization': f'Bearer {api_key}'},
                json={'model': model, 'messages': prompt, 'temperature': 0.01},
                timeout=60000  # Set a timeout of 10 seconds
            )

            response.raise_for_status()

            result = response.json()

            final_result = ''.join(choice['message'].get('content')
                                    for choice in result['choices'])
            return final_result
        except HTTPError as error:
            # Handle specific HTTP errors here
            print(f"HTTP Error occurred: {error}")
            retries += 1
        except requests.exceptions.RequestException as error:
            # Handle other request-related errors here
            print(f"Request Exception occurred: {error}")
            retries += 1
    return None

def query_openai(prompt, model, api_key_value, bot_personality_value):
    """
    Queries the OpenAI API with a given prompt and returns the bot's response.

    Args:
        prompt (str): The prompt to send to the OpenAI API.
        model (str): The ID of the OpenAI model to use.
        api_key_value (str): The API key for the OpenAI API.
        bot_personality_value (str): The personality of the bot to use in the response.

    Returns:
        str: The bot's response to the given prompt.
    """
    prompt = prompt.strip()
    print("\nPROMPT => " + prompt)
    bot_response = open_ai(
        [{
            'role': 'user',
            'content': f'{bot_personality_value} {prompt}'
        }],
        api_key_value,
        model,
        base_url='https://api.openai.com'
    )
    return bot_response

def write_response(response_file, bot_response):
    """
    Writes the bot's response to a text file.

    Args:
        response_file (str): The name of the file to write the response to.
        bot_response (str): The response to write to the file.
    """
    with open(response_file + '.txt', "w", encoding="utf-8") as file:
        file.write(bot_response)

