from .preprocess import preprocess


def make_index(collection):
    inverted_index = dict()

    # Iterate over all colection
    for el in collection:
        # Get tokens from text
        tokens = set(preprocess(el.lyrics))

        # Update inverted_index
        for token in tokens:
            if token in inverted_index:
                inverted_index[token].add(el.filename)
            else:
                inverted_index[token] = {el.filename}

    return inverted_index
