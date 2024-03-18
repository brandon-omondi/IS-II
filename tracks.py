# tracks.py
import os
from flask import Flask, session, redirect, url_for
from spotify_auth import get_spotify_object, handle_auth_flow

app = Flask(__name__)
app.config ['SECRET_KEY'] = os.urandom(64)

@app.route('/')
def home():
    # Call the handle_auth_flow function to handle authentication flow
    handle_auth_flow('user-top-read')
    return redirect(url_for('top_tracks'))    

@app.route('/top_tracks')
def top_tracks():
    # Get the Spotify object from the authentication module
    sp = get_spotify_object('user-top-read')
    
    # Use the Spotify object to retrieve top tracks
    top_tracks = sp.current_user_top_tracks()
    top_tracks_info = [(track['name'], track['external_urls']['spotify']) for track in top_tracks['items']]
    top_tracks_html = '<br>'.join(f'{name}: {url}' for name, url in top_tracks_info)

    return top_tracks_html

@app.route('/logout')
def logout():
    # Clear the session upon logout
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
