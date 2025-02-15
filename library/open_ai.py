""" Funções para usar OpenAi Api
"""

import json
import requests
from requests.exceptions import HTTPError
from openai import OpenAI

def open_ai(system, prompt, api_key, model, max_retries=3) -> str:
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
    client = OpenAI(api_key=api_key, base_url = "https://api.openai.com/v1")
    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": f"{system}"
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}"
                    }
                ],
            )
            result = response.choices[0].message.content
            print(f"Resposta: {result}")

            return result
        except HTTPError as error:
            print(f"HTTP Error occurred: {error}")
            retries += 1
        except requests.exceptions.RequestException as error:
            print(f"Request Exception occurred: {error}")
            retries += 1
        except json.decoder.JSONDecodeError as error:
            print(f"JSON Decode Error occurred: {error}")
            retries += 1
        except AttributeError as error:
            print(f"Attribute Error occurred: {error}")
            retries += 1
    return ''

