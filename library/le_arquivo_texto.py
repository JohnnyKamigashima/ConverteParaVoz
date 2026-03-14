def le_arquivo_texto(arquivo: str) -> str:
    """
    Recebe uma lista de arquivos .txt, concatena o conteúdo deles e retorna uma string.

    :param lista_arquivos: Lista de caminhos para os arquivos .txt.
    :return: String contendo o conteúdo concatenado de todos os arquivos.
    """
    conteudo_arquivo: str = ""

    try:
        with open(arquivo, 'r', encoding='utf-8') as file:
            conteudo_arquivo += file.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo}")
    except OSError as error:
        print(f"Erro ao ler o arquivo {arquivo}: {error}")

    return conteudo_arquivo

