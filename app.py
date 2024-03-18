# app.py

import os
import requests
from flask import Flask, session, redirect, url_for, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SPOTIFY_CLIENT_ID'] = 'd8e5e38bd69348179f5cff944ee8d044'
app.config['SPOTIFY_CLIENT_SECRET'] = 'cd28df8986174d61b5de77e09fc92796'
app.config['SPOTIFY_REDIRECT_URI'] = 'http://localhost:5000/callback'
app.config['SPOTIFY_SCOPE'] = 'playlist-read-private,user-top-read'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=app.config['SPOTIFY_CLIENT_ID'],
    client_secret=app.config['SPOTIFY_CLIENT_SECRET'],
    redirect_uri=app.config['SPOTIFY_REDIRECT_URI'],
    scope=app.config['SPOTIFY_SCOPE'],
    cache_handler=cache_handler
)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))

@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    sp = Spotify(auth_manager=sp_oauth)
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join(f'{name}: {url}' for name, url in playlists_info)

    return playlists_html

@app.route('/get_top_artists')
def get_top_artists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    sp = Spotify(auth_manager=sp_oauth)
    top_artists = sp.current_user_top_artists()
    top_artists_info = [(artist['name'], artist['external_urls']['spotify']) for artist in top_artists['items']]
    top_artists_html = '<br>'.join(f'{name}: {url}' for name, url in top_artists_info)

    return top_artists_html

@app.route('/get_top_tracks')
def get_top_tracks():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    sp = Spotify(auth_manager=sp_oauth)
    top_tracks = sp.current_user_top_tracks()
    top_tracks_info = [(track['name'], track['external_urls']['spotify']) for track in top_tracks['items']]
    top_tracks_html = '<br>'.join(f'{name}: {url}' for name, url in top_tracks_info)

    return top_tracks_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
