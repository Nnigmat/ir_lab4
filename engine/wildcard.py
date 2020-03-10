import re
from .collection import tokens_from_collection


def word_to_bigrams(word, begining=True, ending=True):
    res = []

    # If we got the begining of the word start with '$'
    tmp = '$' if begining else ''

    # Split word into bigrams
    for char in word:
        tmp = tmp + char
        if len(tmp) == 2:
            res.append(tmp)
        tmp = char

    # If we got the ending of the word add '$' to the end
    if ending:
        # Add the last character folowing by '$'
        res.append(tmp + '$')

    return res


def make_bigramex(collection):
    bigramex = dict()

    # Get set of tokens
    tokens = tokens_from_collection(collection, lemma=False)

    # Add tokens to its bigrams
    for token in tokens:
        for bigram in word_to_bigrams(token):
            if bigram not in bigramex:
                bigramex[bigram] = [token]
            else:
                bigramex[bigram].append(token)

    return bigramex


def wildcard_search(pattern, bigramex):
    assert '*' in pattern
    assert len(pattern) > 0

    # Divide word into parts separated by wildcards
    parts = pattern.strip().rstrip().split('*')

    # Take begining and ending parts
    begin, end = parts.pop(0), parts.pop(-1)

    # Filter parts with '' and one symbol
    parts = filter(lambda part: part != '' or len(part) != 1, parts)
    
    # Get all bigrams
    bigrams = set()
    for part in parts:
        bigrams |= set(word_to_bigrams(part, begining=False, ending=False))

    # Put begining and ending to bigrams set
    if len(begin) != 0:
        bigrams |= set(word_to_bigrams(begin, begining=True, ending=False))
    if len(end) != 0:
        bigrams |= set(word_to_bigrams(end, begining=False, ending=True))

    # Get all words that sutisfy bigrams
    start = bigrams.pop()
    words = set()
    if start in bigramex:
        words |= set(bigramex[start])
        for bigram in bigrams:
            words &= set(bigramex[bigram])


    # Filter using regex
    pattern = pattern.replace('*', '.*?')
    res = []
    for word in words:
        if re.fullmatch(pattern, word):
            res.append(word)
    return res
