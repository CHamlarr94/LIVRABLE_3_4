from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    songs = db.relationship('Song', secondary='playlist_song', backref=db.backref('playlists', lazy=True))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=False, nullable=False)


playlist_song = db.Table('playlist_song',
                         db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
                         db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
                         )
