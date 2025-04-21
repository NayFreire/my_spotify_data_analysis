import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

def getting_spotify_credentials():
    # Getting the credentials from the .env file
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    # Setting client credentials    
    spotify_oauth = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    
    # Instantiating the Spotify Manager    
    sp = spotipy.Spotify(
        auth_manager=spotify_oauth
    )
    
    return sp


