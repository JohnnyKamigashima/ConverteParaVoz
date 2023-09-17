"""Text manipulation functions
"""
import re
def limpar_linhas_vazias(texto):
    """
    Removes empty lines from a given text.

    Args:
        texto (str): The text to be processed.

    Returns:
        str: The text without empty lines.
    """
    if texto is None:
        return ""
    if not isinstance(texto, str):
        raise TypeError("Input must be a string")
    linhas = texto.splitlines()
    linhas_limpas = [line for line in linhas if line.strip()]
    texto_limpo = "\n".join(linhas_limpas).strip()
    return texto_limpo


def remove_emojis(text):
    """
    Remove emojis from the given text.

    Args:
        text (str): The input text.

    Returns:
        str: The text with emojis removed.

    Raises:
        TypeError: If the input text is not a string.
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)

    if not isinstance(text, str):
        return None

    if text == '':
        return ''

    return emoji_pattern.sub(r'', text)

def remover_quebras_duplas_e_espacos(string: str) -> str:
    """
    Removes duplicate line breaks and duplicate spaces from a given string.

    Args:
        string (str): The input string that may contain duplicate line breaks and spaces.

    Returns:
        str: The input string with duplicate line breaks and spaces removed.
    """
    if string is None or string == "":
        return string

    try:
        modified_string = re.sub(r'\n+| +', ' ', string)
    except re.error as error:
        print(f"Regex error: {error}")
        modified_string = string

    return modified_string
