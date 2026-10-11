import lyricsgenius
import os
import time
from dotenv import load_dotenv
import pandas as pd
import re

# Getting only the song name from the song title
def remove_feats(name): 
    pattern = r'\s\(*feat.*\s' # pattern for the part of the title where there is a space, maybe a (, the term "feat." and another space
    name = name.lower()
    name = name.split(' - A COLORS SHOW')[0]
    return re.split(pattern, name)[0] # returns the song name, which come before the features

def getting_genius_token():
    load_dotenv()
    return os.getenv("GENIUS_ACCESS_TOKEN")

def reading_csv_files():
    all_tracks_df = pd.read_csv('data\\tracks.csv') # reading the file of individual tracks and turning it into a df. Using subset to add a few lyrics at a time 
    tracking_df = pd.read_csv('data\\spotify_tracking.csv') # reading the file for tracking and turning it into a df
    lyrics_df = pd.read_csv('data\\lyrics.csv')

    return all_tracks_df, tracking_df, lyrics_df

# Reading all the csv files
all_tracks_df, tracking_df, lyrics_df = reading_csv_files()

# Getting Genius id, secrete and token
genius_access_token = getting_genius_token()

genius = lyricsgenius.Genius(genius_access_token, sleep_time=1.0, retries=3, timeout=10) # user authentication for Genius

for track in all_tracks_df.itertuples(): # going through the individual songs df 
    print(tracking_df[tracking_df['id'] == track.track_id], track.track_id)

    current_track = tracking_df[tracking_df['id'] == track.track_id].iloc[0] # to get the track's data from the tracking df

    if track.track_id not in lyrics_df['song_spotify_id'].values: # verifying if the track's lyrics was already added

        artist_name_corrected = current_track.artist_name.split("'")[1] # getting the artist's name, 'cause it's saved as a list. eg: ['Ciara', 'Chamillionaire']. The [1] is to get "Ciara", since [0] is "'" and just the first artist is needed, 'cause they are the main artist

        print(current_track['name'], ' by ', artist_name_corrected) # printing the song name and artist

        new_song = {}

        # Getting Genius Artist
        artist = genius.search_artist(
            artist_name_corrected,
            max_songs=1 # for some reason, it says that max_songs is optional, but it takes too long without it
        )

        # Verifying if the artist exists on Genius
        if (not artist) or (artist_name_corrected.lower() != artist.name.lower()): # if the artists doesn't exist or if the artist returned is not the one we wand (artist_name_corrected)
            print(current_track['name'], ' by ', artist_name_corrected,' NOT FOUND')

        else:        
            song_name = remove_feats(current_track['name']) # remove features from song name (It messes with the search)
            song = genius.search_song(song_name, artist.name) # and get song from Genius by said artist

            # Verifying if the song exists on Genius by said artist
            if (not song) or (song.artist.lower() != artist.name.lower()): #if the song doesn't exist or if the song returned is not the one we want
                print('NO LYRICS')
                new_song = { # create a dictionary with the data we have for the song
                    'song_spotify_id': track.track_id, 
                    'song_name': current_track['name'], 
                    'song_genius_id': None, 
                    'artist_genius_id': artist._body['id'],
                    'artist_spotify_id': current_track.artist_id.split("'")[1],
                    'artist_name': artist_name_corrected,
                    'song_lang': None, 
                    'song_genius_url': None, 
                    'song_lyrics': None
                }

            else:
                new_song = { # create a dictionary with all the song's data
                    'song_spotify_id': track.track_id, 
                    'song_name': current_track['name'], 
                    'song_genius_id': song._body['id'], 
                    'artist_genius_id': artist._body['id'],
                    'artist_spotify_id': current_track.artist_id.split("'")[1],
                    'artist_name': artist_name_corrected,
                    'song_lang': song._body['language'], 
                    'song_genius_url': song.url, 
                    'song_lyrics': song.lyrics
                }
                print(new_song)

            pd.DataFrame([new_song], columns=['song_spotify_id', 'song_name', 'song_genius_id', 'artist_genius_id', 'artist_spotify_id', 'artist_name','song_lang','song_genius_url', 'song_lyrics']).to_csv('data/lyrics.csv', mode='a', index=False, header=not os.path.exists('data/artists_genres.csv'))
        print('X' * 20)

        time.sleep(5) # wait for 5 seconds to do it for the next song on the df
