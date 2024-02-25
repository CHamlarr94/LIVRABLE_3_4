from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from model import Playlist, Song, playlist_song, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.app_context().push()
with app.app_context():
    db.create_all()

client_credentials_manager = SpotifyClientCredentials(client_id='f2294be1b0fd4c5aa73b11bc27549df6',
                                                      client_secret='4c3e190233dc4160b553f5b2fb338e39')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Dans app.py
@app.route('/')
def home():
    playlists = Playlist.query.all()
    return render_template('home.html', playlists=playlists)


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    playlist_name = request.form.get('playlist_name')
    playlist = Playlist(name=playlist_name)
    db.session.add(playlist)
    db.session.commit()
    return render_template('success.html')


# Dans app.py
@app.route('/playlist/<int:playlist_id>')
def playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist is None:
        return "Playlist not found", 404
    return render_template('playlist.html', playlist=playlist)


@app.route('/add_song/<int:playlist_id>', methods=['POST'])
def add_song(playlist_id):
    song_title = request.form.get('song_title')
    playlist = Playlist.query.get(playlist_id)
    if playlist is None:
        return "Playlist not found", 404
    song = Song(title=song_title)
    playlist.songs.append(song)
    db.session.commit()
    return redirect(url_for('playlist', playlist_id=playlist_id))


@app.route('/update_playlist/<int:playlist_id>', methods=['POST'])
def update_playlist(playlist_id):
    new_name = request.form.get('new_name')
    playlist = Playlist.query.get(playlist_id)
    if playlist is None:
        return "Playlist not found", 404
    playlist.name = new_name
    db.session.commit()
    return redirect(url_for('playlist', playlist_id=playlist_id))


@app.route('/update_song/<int:song_id>', methods=['POST'])
def update_song(song_id):
    new_title = request.form.get('new_title')
    song = Song.query.get(song_id)
    if song is None:
        return "Song not found", 404
    song.title = new_title
    db.session.commit()
    return "Song updated", 200


@app.route('/delete_playlist/<int:playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if playlist is None:
        return "Playlist not found", 404
    db.session.delete(playlist)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete_song/<int:song_id>', methods=['POST'])
def delete_song(song_id):
    song = Song.query.get(song_id)
    if song is None:
        return "Song not found", 404
    db.session.delete(song)
    db.session.commit()
    return "Song deleted", 200


@app.route('/search_song', methods=['POST'])
def search_song():
    song_title = request.form.get('song_title')
    playlist_id = request.form.get('playlist_id')
    results = sp.search(q=song_title, limit=10, type='track')
    songs = results['tracks']['items']
    return render_template('search_results.html', songs=songs, playlist_id=playlist_id)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
