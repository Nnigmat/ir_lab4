from flask import Flask, request, render_template
from utils import search, load_song, update
from crawler import checker
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def process_query():
    filenames = search(request.form.get('query'))
    songs = list(map(load_song, filenames))

    return render_template('links.html', songs=songs)


@app.route('/doc/<string:filename>')
def show_document(filename):
    try:
        song = load_song(filename)
    except:
        return 'No such document'

    return render_template('song.html', song=song)


if __name__ == '__main__':
    sched = BackgroundScheduler(daemon=True, max_instances=6)
    sched.add_job(update, 'interval', seconds=5)
    sched.add_job(checker, 'interval', seconds=30)
    sched.start()

    app.run()
