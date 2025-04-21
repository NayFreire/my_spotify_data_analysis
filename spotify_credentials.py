import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

def get_env_sp_credentials():
    # Getting the credentials from the .env file
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    return client_id, client_secret

def get_sp_credentials():
    client_id, client_secret = get_env_sp_credentials()
    
    # Setting client credentials    
    spotify_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='http://127.0.0.1:3000/callback',
        scope='user-read-recently-played'
    )
    
    # Instantiating the Spotify Manager    
    sp = spotipy.Spotify(
        auth_manager=spotify_oauth
    )
    
    return sp