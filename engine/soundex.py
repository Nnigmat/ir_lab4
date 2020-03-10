from .collection import tokens_from_collection


def translate_word(word):
    mappings = {
        'aeiouhwy': '0',
        'bfpv': '1',
        'cgjkqsxz': '2',
        'dt': '3',
        'l': '4',
        'mn': '5',
        'r': '6'
    }

    tmp1 = ''

    # Process each character in token starting from 2nd symbol
    for char in word[1:]:

        # Go through all mappings and change symbol to number
        for key, value in mappings.items():
            if char in key:
                tmp1 = tmp1 + value


    # Remove same sequences of numbers
    prev = ''
    tmp2 = ''
    for char in tmp1:
        if char == prev:
            continue
        else:
            tmp2 = tmp2 + char
            prev = char

    # Remove all zeroes and add the first letter to the begining
    tmp3 = word[0] + tmp2.replace('0', '')

    # Cut string to 4 symbols, if the lenght is less than 4 add 0
    res = tmp3[:4] if len(tmp3) >= 4 else tmp3 + '0' * (4 - len(tmp3))

    return res


def make_soundex(collection):
    soundex = dict()

    tokens = tokens_from_collection(collection)

    # Process each token
    for token in tokens:
        soundexed_word = translate_word(token)

        # Add word to the soundex
        if soundexed_word not in soundex:
            soundex[soundexed_word] = [token]
        else:
            soundex[soundexed_word].append(token)

    return soundex


def soundex_search(word, soundex):
    soundexed_word = translate_word(word)
    return soundex[soundexed_word] if soundexed_word in soundex else []
