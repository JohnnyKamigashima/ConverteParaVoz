from unidecode import unidecode


def limpa_titulo(titulo:str, maximo_caracteres:int):
    """
    Removes the first line of a given text.

    Args:
        titulo (str): The text to be processed.
        maximo_caracteres (int): The maximum number of characters allowed in a line.
        """

    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*' ]

    for char in invalid_chars:
        titulo = titulo.replace(char, '')
        titulo = titulo.replace(' ', '_')
    return unidecode(titulo)[:maximo_caracteres]