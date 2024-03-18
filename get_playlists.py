# # get_playlists.py
# import os
# from flask import Flask, session, redirect, url_for
# from spotipy.cache_handler import FlaskSessionCacheHandler
# from spotify_auth import get_spotify_object, handle_auth_flow

# app = Flask(__name__)
# app.config ['SECRET_KEY'] = os.urandom(64)
# cache_handler = FlaskSessionCacheHandler(session)

# @app.route('/')
# def home():
#     # Call the handle_auth_flow function to handle authentication flow
#     handle_auth_flow('playlist-read-private', cache_handler)
#     return redirect(url_for('get_playlists'))    

# @app.route('/get_playlists')
# def get_playlists():
#     # Get the Spotify object from the authentication module
#     sp = get_spotify_object('playlist-read-private')
    
#     # Use the Spotify object to retrieve user playlists
#     playlists = sp.current_user_playlists()
#     playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
#     playlists_html = '<br>'.join(f'{name}: {url}' for name, url in playlists_info)

#     return playlists_html

# @app.route('/logout')
# def logout():
#     # Clear the session upon logout
#     session.clear()
#     return redirect(url_for('home'))

# if __name__ == '__main__':
#     app.run(debug=True)

#---------------------------------------V1-----------------------------------------#

# get_playlists.py

import os
from flask import Flask, session, redirect, url_for
from spotipy.cache_handler import FlaskSessionCacheHandler
from spotify_auth import get_spotify_object, handle_auth_flow

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

# Initialize the FlaskSessionCacheHandler
cache_handler = FlaskSessionCacheHandler(session)

@app.route('/')
def home():
    # Call the handle_auth_flow function to handle authentication flow
    # Pass the correct arguments: scope and the SpotifyOAuth object
    handle_auth_flow(['playlist-read-private'], get_spotify_object(cache_handler))
    return redirect(url_for('get_playlists'))    

@app.route('/get_playlists')
def get_playlists():
    # Get the Spotify object from the authentication module
    sp = get_spotify_object(cache_handler)
    
    # Use the Spotify object to retrieve user playlists
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join(f'{name}: {url}' for name, url in playlists_info)

    return playlists_html

@app.route('/logout')
def logout():
    # Clear the session upon logout
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
