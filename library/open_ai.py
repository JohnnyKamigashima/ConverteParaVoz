""" Funções para usar OpenAi Api
"""

import requests
from requests.exceptions import HTTPError
def open_ai(prompt, api_key, model, base_url):
    """
    Improved version of the open_ai function.

    Args:
        prompt (str): The prompt for the OpenAI API.
        api_key (str): The API key for authentication.
        model (str): The model to use for the API request.
        base_url (str): The base URL for the API request.

    Returns:
        str: The final result from the API response.
    """

    try:
        # Make the request to the OpenAI API
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
    except requests.exceptions.RequestException as error:
        # Handle other request-related errors here
        print(f"Request Exception occurred: {error}")
    return None
