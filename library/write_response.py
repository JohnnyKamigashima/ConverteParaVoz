def write_response(response_file: str, bot_response: str) -> str:
    """
    Writes the bot's response to a text file.

    Args:
        response_file (str): The name of the file to write the response to.
        bot_response (str): The response to write to the file.
    """
    output_path: str = response_file + '.txt'
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(bot_response)
    return output_path