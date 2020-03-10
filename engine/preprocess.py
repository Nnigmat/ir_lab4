import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Download Stopwords and Words
nltk.download('wordnet')
nltk.download('stopwords')


# normilize text
def normalize(text):
    text = text.lower()
    return ' '.join(re.findall('\w+', text))


def tokenize(text):
    return text.split()


def lemmatization(tokens):
    lemmatizer = WordNetLemmatizer()

    return list(map(lemmatizer.lemmatize, tokens))


def remove_stop_word(tokens):
    return list(set(tokens) - set(stopwords.words('english')))


def preprocess(text, lemma=True):
    text = normalize(text)
    tokens = tokenize(text)
    if lemma:
        tokens = lemmatization(tokens)
    return remove_stop_word(tokens)
