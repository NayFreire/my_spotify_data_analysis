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
    return re.split(pattern, name)[0] # returns the song name, which come before the features

all_tracks_df = pd.read_csv('data\\tracks.csv') # reading the file of individual tracks and turning it into a df
tracking_df = pd.read_csv('data\\spotify_tracking.csv') # reading the file for tracking and turning it into a df

# Getting Genius id, secrete and token
load_dotenv()
genius_client_id = os.getenv("GENIUS_CLIENT_ID")
genius_client_secrete = os.getenv("GENIUS_CLIENT_SECRET")
genius_access_token = os.getenv("GENIUS_ACCESS_TOKEN")

genius = lyricsgenius.Genius(genius_access_token) # user authentication for Genius

songs_lyrics_list = [] # creating a list to archive the song data from Genius

for track in all_tracks_df.itertuples(): # going through the individual songs df 
    current_track = tracking_df[tracking_df['id'] == track.track_id].iloc[0] # to get the track's data from the tracking df

    artist_name_corrected = current_track.artist_name.split("'")[1] # getting the artist's name, 'cause it's saved as a list. eg: ['Ciara', 'Chamillionaire']. The [1] is to get "Ciara", since [0] is "'" and just the first artist is needed, 'cause they are the main artist

    print(current_track['name'], ' by ', artist_name_corrected) # printing the song name and artist

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

            songs_lyrics_list.append(new_song) # and add it to the list that archives all songs
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
            songs_lyrics_list.append(new_song) # and add it to the list that archives all songs

    print('X' * 20)

    time.sleep(5) # wait for 5 seconds to do it for the next song on the df

# Creating a .csv file with the list of archived songs
pd.DataFrame(songs_lyrics_list).to_csv('data/song_lyrics.csv')

# TODO: VERIFY IF A SONG WAS ALREADY ADDED TO THE FILE AND, IF SO, NOT ADD IT AGAIN