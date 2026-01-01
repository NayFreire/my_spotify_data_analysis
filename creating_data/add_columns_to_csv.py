from csv_file import read_csv_file
from getting_recently_played_songs import getting_genres, getting_albums
import ast
import pandas as pd

csv_data = pd.DataFrame(read_csv_file())

def getting_genres_column(df):
    genres_column = []
    print('ADDING GENRES')
    for track in df.itertuples():
        print('in genre', track)
        list_values = ast.literal_eval(track.artist_id)
        genres = getting_genres(list_values)        
        genres_column.append(genres)

    return genres_column

def getting_album_column(df):
    album_info_id = []
    album_info_name = []
    album_info_date = []
    album_info_type = []
    print('ADDING ALBUM RELATED COLUMNS')
    for track in df.itertuples():
        album = getting_albums(track.id)
        print('in album', track)
        if album is None:
            album_info_id.append(None)
            album_info_name.append(None)
            album_info_date.append(None)
            album_info_type.append(None)
        else:
            album_info_id.append(album['id'])
            album_info_name.append(album['name'])
            album_info_date.append(album['release_date'])
            album_info_type.append(album['album_type'])

    return album_info_id, album_info_name, album_info_date, album_info_type

# Getting the 'genre' column
csv_data['genre'] = getting_genres_column(csv_data)

# Getting the 'album' related columns
album_id, album_name, album_date, album_type = getting_album_column(csv_data)

csv_data['album_id'] = album_id
csv_data['album_name'] = album_name
csv_data['album_release_date'] = album_date
csv_data['album_type'] = album_type


csv_data.to_csv('data/updated_spotify_tracking.csv')
