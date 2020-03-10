def get_same_words(word, soundex):
    # Translate word into soundex format and get all same ones
    translation = translate_word(word)
    words = soundex[translation]
    
    # Calculate closenes of each word to initial
    closenes = []
    for w in words:
        closenes.append(levenstein_distance(w, word))
    

    # Get the words with minimal value
    res = []
    for i, w in enumerate(words):
        if closenes[i] == min(closenes):
            res.append(w)

    return res
