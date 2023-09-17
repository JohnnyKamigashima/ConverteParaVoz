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

def substituir_quebras_de_linha(texto, caracteres):
    """
        Generate a function comment for the given function body in a markdown
        code block with the correct language syntax.

        Parameters:
            texto (str): The input text to be processed.
            caracteres (int): The maximum number of characters allowed in a line.

        Returns:
            str: The processed text with line breaks substituted.
    """
    # Adicionar ponto final no final de cada frase
    texto = texto.replace(". ", ".\n")

    # Substituir quebra de linha simples por ponto e espaço
    texto = texto.replace("\n", ". ")

    # Substituir duas quebras de linha por uma quebra única
    texto = texto.replace("\n\n", "\n")

    # Remover quebras de linha quando a linha tiver menos de 200 caracteres
    linhas = texto.split("\n")
    linhas_formatadas = []
    for linha in linhas:
        if len(linha) < caracteres:
            linha = linha.replace("\n", " ")
        linhas_formatadas.append(linha)
    texto = "\n".join(linhas_formatadas)

    return texto

def adicionar_quebras_de_linha(texto, caracteres):
    """
    Splits a given text into multiple lines, inserting line breaks
    after a certain number of characters.

    Args:
        texto (str): The text to be formatted.
        caracteres (int): The number of characters after which a line break should be inserted.

    Returns:
        str: The formatted text with line breaks inserted.

    """
    linhas = texto.split("\n")
    linhas_formatadas = []
    for linha in linhas:
        if len(linha) > caracteres:
            nova_linha = ""
            palavras = linha.split(".")
            contador = 0
            for palavra in palavras:
                nova_linha += palavra + "."
                contador += len(palavra) + 1
                if contador > caracteres:
                    nova_linha += "\n"
                    contador = 0
            linhas_formatadas.append(nova_linha)
        else:
            linhas_formatadas.append(linha)
    texto_formatado = "\n".join(linhas_formatadas)
    return texto_formatado
