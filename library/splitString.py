MAX_PHRASE_LENGTH: int = 256


def divide_frases(long_string: str) -> list[str]:
    """Divide um texto em blocos de tamanho controlado para sintetizacao de voz."""
    phrases: list[str] = long_string.split("\n")
    result: list[str] = []
    current_phrase: str = ""

    for phrase in phrases:
        if len(current_phrase) + len(phrase) + 1 <= MAX_PHRASE_LENGTH:
            current_phrase += phrase + ". "
        else:
            result.append(current_phrase.strip())
            current_phrase = phrase + ". "

    if current_phrase.strip():
        result.append(current_phrase.strip())

    return result