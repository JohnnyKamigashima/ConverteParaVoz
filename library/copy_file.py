"""Copia arquivos
"""
import shutil
def copy_file(source_file, destination_file):
    """
    Copy a file from the source path to the destination path.

    Args:
        source_file (str): The path of the source file to be copied.
        destination_file (str): The path where the source file should be copied to.

    Returns:
        None
    """
    shutil.copyfile(source_file, destination_file)
    