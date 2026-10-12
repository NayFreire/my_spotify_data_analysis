import lyricsgenius
import os
import time
from dotenv import load_dotenv
import pandas as pd
import re
import numpy as np
import requests as req

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

def getting_track_lyrics(track):
    # Getting Genius id, secrete and token
    genius_access_token = getting_genius_token()

    genius = lyricsgenius.Genius(genius_access_token, sleep_time=1.0, retries=3, timeout=10) # user authentication for Genius

    artist_name_corrected = track.artist_name[0] # getting the artist's name, 'cause it's saved as a list. eg: ['Ciara', 'Chamillionaire']. The [1] is to get "Ciara", since [0] is "'" and just the first artist is needed, 'cause they are the main artist

    print(track.name, ' by ', artist_name_corrected) # printing the song name and artist

    new_song = {}

    # Getting Genius Artist
    artist = genius.search_artist(
        artist_name_corrected,
        max_songs=1 # for some reason, it says that max_songs is optional, but it takes too long without it
    )

    # Verifying if the artist exists on Genius
    if (not artist) or (artist_name_corrected.lower() != artist.name.lower()): # if the artists doesn't exist or if the artist returned is not the one we want (artist_name_corrected)
        print(track.name, ' by ', artist_name_corrected,' NOT FOUND ON GENIUS')

    else:        
        song_name = remove_feats(track.name) # remove features from song name (It messes with the search)
        song = genius.search_song(song_name, artist.name) # and get the song from Genius by said artist

        # Verifying if the song exists on Genius by said artist
        if (not song) or (song.artist.lower() != artist.name.lower()): #if the song doesn't exist or if the song returned is not the one we want
            print('NO LYRICS')
            new_song = { # create a dictionary with the data we have for the song
                'song_spotify_id': track.id, 
                'song_name': track.name, 
                'song_genius_id': None, 
                'artist_genius_id': artist._body['id'],
                'artist_spotify_id': track.artist_id[0],
                'artist_name': artist_name_corrected,
                'song_lang': None, 
                'song_genius_url': None, 
                'song_lyrics': None
            }

        else:
            new_song = { # create a dictionary with all the song's data
                'song_spotify_id': track.id, 
                'song_name': track.name, 
                'song_genius_id': song._body['id'], 
                'artist_genius_id': artist._body['id'],
                'artist_spotify_id': track.artist_id[0],
                'artist_name': artist_name_corrected,
                'song_lang': song._body['language'], 
                'song_genius_url': song.url, 
                'song_lyrics': song.lyrics
            }
            print(new_song)

    print('X' * 20)

    time.sleep(5) # wait for 5 seconds to do it for the next song on the df
    return new_song

def adding_instrumental_column():
    lyrics_df = pd.DataFrame(pd.read_csv('data\\lyrics.csv'))
    # print(lyrics_df)

    lyrics_df.rename(columns={
        'song_genius_id': 'source_track_id',
        'artist_genius_id': 'source_artist_id',
        'song_genius_url': 'source_track_url'
    }, inplace=True)

    # print(lyrics_df.columns)


    lyrics_df['instrumental'] = lyrics_df['song_lyrics'].isna()
    lyrics_df['source'] = np.where(
        lyrics_df['source_track_url'].notna(),
        'Genius',
        None
    )
    # print(lyrics_df)

    base_url = 'https://lrclib.net'

    no_lyrics_df = lyrics_df[lyrics_df['song_lyrics'].isna()]
    print(no_lyrics_df)

    lyrics_list = []
    
    for track in lyrics_df.itertuples():
        print(track)
        if pd.isna(track.song_lyrics):
            artist = track.artist_name.replace(' ', '+')
            song = track.song_name.replace(' ', '+')

            track_data = req.get(f'{base_url}/api/get?artist_name={artist}&track_name={song}')

            # print(track_data.status_code, track_data.content,'\n\n')
            if track_data.status_code == 200:
                track_data = track_data.json()
                # print(track_data)
                track_response = {
                    'id': track_data['id'],
                    'instrumental': track_data['instrumental'],
                    'lyrics': track_data['plainLyrics']
                }

                print(track_data['name'])
                new_song = {
                    'song_spotify_id': track.song_spotify_id, 
                    'song_name': track.song_name, 
                    'source_track_id': track_data['id'], 
                    'source_artist_id': None,
                    'artist_spotify_id': track.artist_spotify_id,
                    'artist_name': track.artist_name,
                    'song_lang': track.song_lang, 
                    'source_track_url': f'{base_url}/api/get?artist_name={artist}&track_name={song}', 
                    'song_lyrics': track_data['plainLyrics'],
                    'instrumental': track_data['instrumental'],
                    'source': 'lrclib'
                }
                lyrics_list.append(new_song)
            else:
                track_data = track_data.json()
                print(track.song_name, 'by', track.artist_name, 'NOT FOUND\n', track_data['message'])
                new_song = {
                    'song_spotify_id': track.song_spotify_id, 
                    'song_name': track.song_name, 
                    'source_track_id': track.source_track_id, 
                    'source_artist_id': track.source_artist_id,
                    'artist_spotify_id': track.artist_spotify_id,
                    'artist_name': track.artist_name,
                    'song_lang': track.song_lang, 
                    'source_track_url': track.source_track_url, 
                    'song_lyrics': track.song_lyrics,
                    'instrumental': True,
                    'source': None
                }
        else:
            new_song = {
                'song_spotify_id': track.song_spotify_id, 
                'song_name': track.song_name, 
                'source_track_id': track.source_track_id, 
                'source_artist_id': track.source_artist_id,
                'artist_spotify_id': track.artist_spotify_id,
                'artist_name': track.artist_name,
                'song_lang': track.song_lang, 
                'source_track_url': track.source_track_url, 
                'song_lyrics': track.song_lyrics,
                'instrumental': False,
                'source': 'Genius'
            }
        lyrics_list.append(new_song)

    pd.DataFrame(lyrics_list).drop_duplicates().to_csv('data\\source_test.csv', index=False)

    

adding_instrumental_column()