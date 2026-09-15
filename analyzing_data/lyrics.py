import lyricsgenius
import os
import time
from dotenv import load_dotenv
import pandas as pd

def remove_feats(name):
    return name.split(' (feat.')[0]

all_tracks_df = pd.read_csv('data\\tracks.csv')
tracking_df = pd.read_csv('data\\spotify_tracking.csv')

# print(df)

load_dotenv()
genius_client_id = os.getenv("GENIUS_CLIENT_ID")
genius_client_secrete = os.getenv("GENIUS_CLIENT_SECRET")
genius_access_token = os.getenv("GENIUS_ACCESS_TOKEN")

genius = lyricsgenius.Genius(genius_access_token)

songs_lyrics_list = []

for track in all_tracks_df.itertuples():
    # print(track)
    current_track = tracking_df[tracking_df['id'] == track.track_id].iloc[0]
    # print(current_track)

    artist_name_corrected = current_track.artist_name.split("'")[1]

    print(current_track['name'], ' by ', artist_name_corrected)
    
    artist = genius.search_artist(
        artist_name_corrected,
        max_songs=1
    )
    # print(artist._body)

    aaa = artist_name_corrected.lower() != artist.name.lower()

    if (not artist) or (artist_name_corrected.lower() != artist.name.lower()):
        print(current_track['name'], ' by ', artist_name_corrected,' NOT FOUND')
    else:        
        song_name = remove_feats(current_track['name'])
        song = genius.search_song(song_name, artist.name)

        if (not song) or (song.artist.lower() != artist.name.lower()):
            print('NO LYRICS')
            new_song = {
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
            songs_lyrics_list.append(new_song)
        else:
            # print(song.lyrics)
            new_song = {
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
            songs_lyrics_list.append(new_song)

    print('X' * 20)

    time.sleep(5)


pd.DataFrame(songs_lyrics_list).to_csv('data/song_lyrics.csv')

# TODO: VERIFY IF A SONG WAS ALREADY ADDED TO THE FILE AND, IF SO, NOT ADD IT AGAIN