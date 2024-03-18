# # spotify_auth.py

# import os
# from flask import session, redirect, url_for
# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyOAuth
# from spotipy.cache_handler import FlaskSessionCacheHandler

# def get_spotify_object(scope):
#     app_client_id = '4941399b4ff9443baf7d6686604fb36e'
#     app_client_secret = 'b71db7142aa54208af1db6478659b3fa'
#     redirect_uri = 'http://localhost:5000/callback'

#     cache_handler = FlaskSessionCacheHandler(session)
#     sp_oauth = SpotifyOAuth(
#         client_id=app_client_id,
#         client_secret=app_client_secret,
#         redirect_uri=redirect_uri,
#         scope=scope,
#         cache_handler=cache_handler,
#         show_dialog=True
#     )
    
#     if 'token_info' in session:
#         token_info = session['token_info']
#     else:
#         token_info = None

#     sp = Spotify(auth_manager=sp_oauth, token_info=token_info)

#     if token_info and sp_oauth.is_token_expired(token_info):
#         token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
#         session['token_info'] = token_info

#     return sp

# def handle_auth_flow(scope):
#     sp_oauth = get_spotify_object(scope)
    
#     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)

# V1

# spotify_auth.py

import os
from flask import session, redirect, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

def get_spotify_object(scope):
    app_client_id = '4941399b4ff9443baf7d6686604fb36e'
    app_client_secret = 'b71db7142aa54208af1db6478659b3fa'
    redirect_uri = 'http://localhost:5000/callback'

    cache_handler = FlaskSessionCacheHandler(session)
    sp_oauth = SpotifyOAuth(
        client_id=app_client_id,
        client_secret=app_client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_handler=cache_handler,
        show_dialog=True
    )
    
    if 'token_info' in session:
        token_info = session['token_info']
    else:
        token_info = None

    sp = Spotify(auth_manager=sp_oauth)  # Initialize Spotify object with SpotifyOAuth instance

    if token_info and sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info

    return sp


# def handle_auth_flow(scope, cache_handler):
#     sp_oauth = get_spotify_object(scope)
    
#     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)
# V1

# def handle_auth_flow(scope, cache_handler):
#     sp_oauth = get_spotify_object(scope)
    
#     if not cache_handler.get_cached_token() or not sp_oauth.is_token_valid(cache_handler.get_cached_token()):        
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)
# V2

# def handle_auth_flow(scope, sp_oauth):
#     if not sp_oauth.validate_token(session.get('token_info')):
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)
#V3

def handle_auth_flow(scope, sp_oauth):
    token_info = session.get('token_info')
    if not token_info or not sp_oauth.is_token_valid(token_info):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)



