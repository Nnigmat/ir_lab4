import requests as r
from bs4 import BeautifulSoup
import urllib.parse
from .preprocess import preprocess
from pickle import dump
from os.path import exists
from hashlib import md5

folder = 'engine/collection/'


def document_present(link):
    return exists(folder + md5(link.encode()).hexdigets())


def get_collection(amount=1000):
    counter = 0

    # Get top artist page
    response = r.get('https://www.lyrics.com/topartists.php')
    soup = BeautifulSoup(response.text, features='html.parser')

    # Get table with the artists links
    table = soup.find('table', class_='tdata')

    # Go to artists page
    for a in table.find_all('a'):
        response = r.get(urllib.parse.urljoin(
            'https://www.lyrics.com/', a['href']))
        soup = BeautifulSoup(response.text, features="html.parser")

        # Find all links to songs
        songs = soup.find_all('td', class_='tal qx')
        for song in songs:
            url = urllib.parse.urljoin(
                'https://www.lyrics.com/', song.find('a')['href'])
            if document_present(url):
                continue

            response = r.get(url)
            soup = BeautifulSoup(response.text, features="html.parser")

            # Get artist, title and text of a song
            artist = soup.find('h3', class_='lyric-artist').find('a').text
            title = soup.find('h1', class_='lyric-title').text
            text = soup.find('pre', class_='lyric-body').text

            dump(Song(artist, title, text), open(
                f'{folder}{md5(url.encode()).hexdigets()}', 'wb'))

            counter += 1
            if counter >= amount:
                break

        if counter >= amount:
            break

    return collection


def tokens_from_collection(collection, lemma=True):
    tokens = set()
    # Collect all words from collection
    for song in collection:
        # Preprocess text without lemmatization
        tokens |= set(preprocess(song.lyrics, lemma=lemma))
    return tokens
