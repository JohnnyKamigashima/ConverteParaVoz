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

    # Substituir quebra de linha simples por espaço
    texto = texto.replace("\n", " ")

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