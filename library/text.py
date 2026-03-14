"""Text manipulation functions
"""


def limpar_linhas_vazias(texto: str | None) -> str:
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
    linhas: list[str] = texto.splitlines()
    linhas_limpas: list[str] = [line for line in linhas if line.strip()]
    texto_limpo: str = "\n".join(linhas_limpas).strip()
    return texto_limpo

