from engine.levenstein_distance import levenstein_distance
from engine.preprocess import preprocess
from engine.soundex import make_soundex, soundex_search
from engine.spelling import get_same_words
from engine.wildcard import make_bigramex, wildcard_search
from pickle import dump, load
from os.path import exists
from os import listdir, remove

index_dir = 'index/'
collection_dir = 'collection/'

# Number of elements in a collection
collection_length = 5

# Create bigramex, soundex
bigramex = dict()
soundex = dict()


def update():
    ''' Update bigramex and soundex '''
    global bigramex, soundex

    collection = load_collection()
    bigramex = make_bigramex(collection)
    soundex = make_soundex(collection)


def load_song(filename):
    ''' Load song from collection '''
    path = f'{collection_dir}{filename}'

    if exists(path):
        with open(path, 'rb') as f:
            return load(f)
    else:
        return None


def load_index(token):
    ''' Load inverted index entry '''
    path = f'{index_dir}{token}'

    if exists(path):
        with open(path, 'rb') as f:
            return load(f)
    else:
        return {}


def load_collection():
    ''' Load collection '''
    col_filenames = listdir(collection_dir)
    col_filenames.remove('proceed')

    return list(map(load_song, col_filenames))


def index_has(token):
    ''' Does the inverted index key exist '''
    path = f'{index_dir}{token}'
    return exists(path)


def delete_from_collection(filename):
    path = f'{collection_dir}{filename}'
    remove(path)


def remove_from_index(tokens, filename):
    for token in tokens:
        index = load_index(token)
        index.remove(filename)

        dump(index, open(index_dir + filename, 'wb+'))


def update_index(tokens, filename):
    for token in tokens:
        index = load_index(token)
        index.add(filename)

        dump(index, open(index_dir + filename, 'wb+'))


def search(query):
    relevant_documents = []
    filenames = set()

    tokens = set()

    # Find words with '*' add APScheduler==3.6.3them to tokens and remove from query
    query = query.split()
    for i, word in enumerate(query):
        if '*' in word:
            tokens.add(word)
            query.pop(i)

    # Preprocess words without '*'
    tokens |= set(preprocess(' '.join(query), lemma=False))

    # Process each token
    for i, token in enumerate(tokens):
        tmp = set()
        words = []

        # If token in index ok.
        # If '*' in token search in wildcard
        # Otherwise search in soundex

        if index_has(token):
            tmp = load_index(token)
        elif '*' in token:
            words = wildcard_search(token, bigramex)
        else:
            words = soundex_search(token, soundex)

        # Process each similar words to token (found in wildcard and soundex)
        for word in words:
            if index_has(word):
                tmp |= load_index(word)

        if i == 0:
            filenames = tmp
        else:
            filenames &= tmp

    return filenames
