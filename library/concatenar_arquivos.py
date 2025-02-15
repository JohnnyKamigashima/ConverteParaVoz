def concatenar_arquivos(lista_arquivos):
    """
    Recebe uma lista de arquivos .txt, concatena o conteúdo deles e retorna uma string.

    :param lista_arquivos: Lista de caminhos para os arquivos .txt.
    :return: String contendo o conteúdo concatenado de todos os arquivos.
    """
    conteudo_concatenado = ""

    for arquivo in lista_arquivos:
        try:
            with open(arquivo, 'r', encoding='utf-8') as file:
                conteudo_concatenado += file.read() + "\n"  # Adiciona uma quebra de linha entre os arquivos
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {arquivo}")
        except Exception as e:
            print(f"Erro ao ler o arquivo {arquivo}: {e}")

    return conteudo_concatenado

