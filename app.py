from flask import Flask, render_template,request
from lyrics import scrapeLyricsText
from markov import MarkovLyrics

app = Flask(__name__, template_folder='template')

def generateArtistLyrics(name):
    songs = scrapeLyricsText(name)

    model = MarkovLyrics()
    for song in songs:
        model.populateChain(song)

    lyrics = model.generateLyrics()
    return lyrics.split("NEWLINE")


@app.route('/', methods=['GET','POST'])


def lyricsGenerator():
    song = []
    if request.method == "POST":
        artist = request.form['search']
        song = generateArtistLyrics(artist)

    return render_template('home.html', song=song)


if __name__ == '__main__':
    app.run(debug=True);