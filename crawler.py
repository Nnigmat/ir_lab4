from song import Song
from engine.index import make_index
from engine.collection import preprocess

from bs4 import BeautifulSoup as BS
from os.path import exists
from time import sleep
from pickle import dump, load
import requests as r
from string import ascii_uppercase
from urllib.parse import urljoin
from multiprocessing import Queue, Process, Pool
from utils import load_collection, load_index, delete_from_collection, remove_from_index, update_index
from apscheduler.schedulers.background import BackgroundScheduler


# Size of documents before updating
SIZE = 5

# Folders where stored collection, proceed files, index
COLLECTION = 'collection/'
PROCEED = 'collection/proceed/'
INDEX = 'index/'


# Constants declaration
SITE = 'https://www.lyrics.com/'
ARTISTS = 'https://www.lyrics.com/artists/{letter}/99999'
SYMBOLS = '0' + ascii_uppercase
LIMIT_PER_SYMBOL = 1


def crawler(queue):
    """
    The function collects the songs and stores them into 'collection' folder
    """
    for symbol in SYMBOLS:
        print(symbol)
        count = 0

        # Get the artists begining with 'symbol'
        resp = r.get(ARTISTS.format(letter=symbol))
        soup = BS(resp.text, features='html.parser')
        table = soup.find('table', class_='tdata')

        # Process each artist
        for a in table.find_all('a'):
            # Get it's all albums
            resp = r.get(urljoin(SITE, a['href']))

            # Check that the page exists
            if resp.status_code != 200:
                continue

            # Create soup
            soup = BS(resp.text, features='html.parser')

            # Find all links to songs
            for song in soup.find_all('td', class_='tal qx'):
                if count >= LIMIT_PER_SYMBOL:
                    break

                url = urljoin(SITE, song.find('a')['href'])
                resp = r.get(url)

                # Check that the page exists
                if resp.status_code != 200:
                    continue

                soup = BS(resp.text, features='html.parser')

                # Get artist, title and text from the doc
                artist = soup.find(class_='lyric-artist').text[:-13]
                title = soup.find(class_='lyric-title').text
                lyrics = soup.find(class_='lyric-body').text

                # Create song object
                song = Song(artist, title, lyrics, url)

                # If already proceed pass the doc
                if exists(PROCEED + song.filename):
                    continue

                # Store the song to the hard drive
                with open(COLLECTION + song.filename, 'wb+') as f:
                    dump(song, f)

                # Store that song was proceed
                open(PROCEED + song.filename, 'w+')

                # Notify the user
                print(f'STORED: {song.filename}')

                # Send song to proceed
                queue.put(song)

                count += 1

                # Sleep
                # sleep(0.5)

            if count >= LIMIT_PER_SYMBOL:
                break


def updater(queue, size):
    songs = []

    # Start daemon
    while True:
        songs.append(queue.get())

        # If songs not enough  wait
        if len(songs) < size:
            continue

        # Create index of songs
        index = make_index(songs)

        # Update the index
        for word, docs in index.items():
            path = INDEX + word
            if exists(path):
                # Update the index entry
                with open(path, 'rb+') as f:
                    entry = load(f)
                    entry |= docs
                    dump(entry, f)
            else:
                # Create the index entry
                with open(path, 'wb+') as f:
                    dump(docs, f)


def checker():
    collection = load_collection()
    for song in collection:
        resp = r.get(song.url)

        if resp.status_code != 200:
            delete_from_collection(song.filename)
            remove_from_index(preprocess(
                song.lyrics, lemma=False), song.filename)

        soup = BS(resp.text, features='html.parser')

        # Get artist, title and text from the doc
        artist = soup.find(class_='lyric-artist').text[:-13]
        title = soup.find(class_='lyric-title').text
        lyrics = soup.find(class_='lyric-body').text

        song2 = Song(artist, title, lyrics, song.url)

        ''' !!!! Need to get tokens from the song and subtruct that doesn't in song2!!!!'''
        if song != song2:
            tokens_1 = preprocess(song.lyrics, lemma=False)
            tokens_2 = preprocess(song2.lyrics, lemma=False)

            # Find tokens not presented in updated
            to_remove = tokens_1 - tokens_2
            remove_from_index(to_remove, song.filename)

            # Find tokens that new in updated
            to_update = tokens_2 - tokens_1
            update_index(to_update, song.filename)

        print(f'CHECKED: {song.filename}')


if __name__ == '__main__':
    queue = Queue()

    # Updater initialization
    updater = Process(target=updater, args=((queue, SIZE)))
    updater.daemon = True
    updater.start()

    # Crawler initialization
    crawler(queue)
