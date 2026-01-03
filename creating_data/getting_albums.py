from csv_file import read_csv_file
# from getting_recently_played_songs import getting_genres, getting_albums
from spotify_credentials import get_sp_credentials
import ast
import pandas as pd
import time

csv_data = pd.DataFrame(read_csv_file())

# print(csv_data['artist_id'])

def getting_tracks_chunks(artists_list):
    max_len = 50 # max number of id's per request
    iter_list = artists_list # making a copy of the list, so it can be altered
    lists = []

    iterations = len(artists_list)/max_len
    remaining = iterations - int(iterations)

    print(iterations, len(artists_list), remaining)

    for i in range(int(iterations)+1): # There's a +1 here so the for loop can iterate through the last remaining ids
        print(f'NUMBER OF ITERATIONS: {i}')
        if len(iter_list) >= max_len:
            lists.append(iter_list[0:max_len])
            del iter_list[0:max_len]
        else:
            if(remaining > 0):
                lists.append(iter_list[0:len(iter_list)])
                del iter_list[0:len(iter_list)]
    print(lists)

    return lists

print(csv_data['id'])

def getting_unique_tracks_ids(track_ids_column):
    track_ids = []

    for track_id in track_ids_column:
        print(track_id, type(track_id))
        track_ids.append(track_id)

    track_ids = list(set(track_ids))
    print(f'TOTAL NUMBER OF TRACKS: {len(track_ids)}')

    return track_ids

def getting_tracks_albums(track_ids):
    sp = get_sp_credentials()

    final_tracks_list = []

    for id_list in track_ids:
        result = sp.tracks(id_list)

        for track in result['tracks']:
            final_tracks_list.append(
                {
                    'track_id': track['id'],
                    'album_type': track['album']['album_type'],
                    'album_id': track['album']['id'],
                    'album_name': track['album']['name'],
                    'album_release_date': track['album']['release_date']
                }
            )

        time.sleep(1)
    return final_tracks_list


unique_tracks_id_list = getting_unique_tracks_ids(csv_data['id'])
track_ids = getting_tracks_chunks(unique_tracks_id_list)

tracks_info = getting_tracks_albums(track_ids)

print(tracks_info)

pd.DataFrame(tracks_info).to_csv('data/tracks.csv', index=None)