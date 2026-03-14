def adicionar_quebras_de_linha(texto: str, caracteres: int) -> str:
    """
    Splits a given text into multiple lines, inserting line breaks
    after a certain number of characters.

    Args:
        texto (str): The text to be formatted.
        caracteres (int): The number of characters after which a line break should be inserted.

    Returns:
        str: The formatted text with line breaks inserted.

    """
    if caracteres <= 0:
        raise ValueError("caracteres must be greater than zero")

    linhas: list[str] = texto.split("\n")
    linhas_formatadas: list[str] = []
    for linha in linhas:
        if len(linha) > caracteres:
            nova_linha: str = ""
            palavras: list[str] = linha.split(".")
            contador: int = 0
            for palavra in palavras:
                nova_linha += palavra + "."
                contador += len(palavra) + 1
                if contador > caracteres:
                    nova_linha += "\n"
                    contador = 0
            linhas_formatadas.append(nova_linha)
        else:
            linhas_formatadas.append(linha)
    texto_formatado: str = "\n".join(linhas_formatadas)
    return texto_formatado