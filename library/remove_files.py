import os


def remove_files(file_list) -> None:
    """
    Removes a list of files from the file system.

    Args:
        file_list (list): A list of file paths to be removed.

    Returns:
        None
    """
    for file in file_list:
        if os.path.exists(file):
            os.remove(file)