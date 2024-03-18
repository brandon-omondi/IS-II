# artists.py
import os
from flask import Flask, session, redirect, url_for
from spotify_auth import get_spotify_object, handle_auth_flow

app = Flask(__name__)
app.config ['SECRET_KEY'] = os.urandom(64)

@app.route('/')
def home():
    # Call the handle_auth_flow function to handle authentication flow
    handle_auth_flow('user-top-read')
    return redirect(url_for('top_artists'))    

@app.route('/top_artists')
def top_artists():
    # Get the Spotify object from the authentication module
    sp = get_spotify_object('user-top-read')
    
    # Use the Spotify object to retrieve top artists
    top_artists = sp.current_user_top_artists()
    top_artists_info = [(artist['name'], artist['external_urls']['spotify']) for artist in top_artists['items']]
    top_artists_html = '<br>'.join(f'{name}: {url}' for name, url in top_artists_info)

    return top_artists_html

@app.route('/logout')
def logout():
    # Clear the session upon logout
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
