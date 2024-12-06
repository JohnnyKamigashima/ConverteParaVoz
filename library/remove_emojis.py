import re


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