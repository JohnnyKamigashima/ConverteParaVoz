def le_arquivo_texto(arquivo):
    """
    Recebe uma lista de arquivos .txt, concatena o conteúdo deles e retorna uma string.

    :param lista_arquivos: Lista de caminhos para os arquivos .txt.
    :return: String contendo o conteúdo concatenado de todos os arquivos.
    """
    conteudo_concatenado = ""

    try:
        with open(arquivo, 'r', encoding='utf-8') as file:
            conteudo_concatenado += file.read()   # Adiciona uma quebra de linha entre os arquivos
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo}")
    except Exception as e:
        print(f"Erro ao ler o arquivo {arquivo}: {e}")

    return conteudo_concatenado

