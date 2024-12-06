def write_response(response_file, bot_response):
    """
    Writes the bot's response to a text file.

    Args:
        response_file (str): The name of the file to write the response to.
        bot_response (str): The response to write to the file.
    """
    with open(response_file + '.txt', "w", encoding="utf-8") as file:
        file.write(bot_response)