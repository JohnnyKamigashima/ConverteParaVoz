def divide_frases(long_string):
    phrases = long_string.split('\n')
    result = []
    current_phrase = ''
    for phrase in phrases:
        if len(current_phrase) + len(phrase) + 1 <= 256:
            current_phrase += phrase + '. '
        else:
            result.append(current_phrase.strip())
            current_phrase = phrase + '. '
    result.append(current_phrase.strip())
    return result