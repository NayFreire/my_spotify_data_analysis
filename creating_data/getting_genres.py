from csv_file import read_csv_file
# from getting_recently_played_songs import getting_genres, getting_albums
from spotify_credentials import get_sp_credentials
import ast
import pandas as pd
import time

csv_data = pd.DataFrame(read_csv_file())

# print(csv_data['artist_id'])

def getting_artist_chunk(artists_list):
    max_len = 40 # max number of id's per request
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

def getting_unique_artist_ids(artist_ids_column):
    artist_ids = []

    for artist_id in artist_ids_column:
        print(artist_id, type(artist_id), ast.literal_eval(artist_id))
        for id in ast.literal_eval(artist_id):
            # print(id)
            artist_ids.append(id)

    artist_ids = list(set(artist_ids))
    print(f'TOTAL NUMBER OF ARTISTS: {len(artist_ids)}')
    return artist_ids

def getting_artists_genres(artist_ids):
    final_artists_list = []
    sp = get_sp_credentials()

    for id_list in artist_ids:
        result = sp.artists(id_list)

        for artist in result['artists']:
            final_artists_list.append(
                {
                    'id': artist['id'],
                    'genres': ', '.join(artist['genres']) if artist['genres'] else None
                }
            )
        time.sleep(1)
    return final_artists_list

#! Uncomment the following lines to re-add all the genres to the csv file 
# unique_artist_ids_list = getting_unique_artist_ids(csv_data['artist_id'])
# artist_ids = getting_artist_chunk(unique_artist_ids_list)

# artists_info = getting_artists_genres(artist_ids)

# print(artists_info)

# pd.DataFrame(artists_info).to_csv('data/artists_genres.csv', index=None)