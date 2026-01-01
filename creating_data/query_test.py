from csv_file import read_csv_file
from getting_recently_played_songs import getting_genres, getting_albums
from spotify_credentials import get_sp_credentials
import ast
import pandas as pd

def get_artist_name(df, artist_id):
    for track in df.itertuples():
        if artist_id in track.artist_id:
            print(track)
            list_correction = ast.literal_eval(track.artist_name)
            return track.artist_id.index(artist_id), list_correction[track.artist_id.index(artist_id)]

csv_data = pd.DataFrame(read_csv_file())[0:200]
# print(csv_data['artist_id'])

artist_ids = []

for artist_id in csv_data['artist_id']:
    # print(artist_id, type(artist_id), ast.literal_eval(artist_id))
    for id in ast.literal_eval(artist_id):
        # print(id)
        artist_ids.append(id)

artist_ids = list(set(artist_ids))
# print(artist_ids, len(artist_ids))

csv_data["artist_id"] = csv_data["artist_id"].apply(ast.literal_eval)

print(csv_data["artist_id"])

artists_names = []
list_artists_genres = []

sp = get_sp_credentials()

for artist_id in artist_ids:
    id_index, artist_name = get_artist_name(csv_data, artist_id)
    print(id_index, artist_name)
    artists_names.append(artist_name)

    artists_genres = []
    artist = sp.artist(artist_id)

    if len(artist['genres']) > 0:
        for genre in artist['genres']:
            artists_genres.append(genre)   

    print(artist_id, artist_name, artists_genres)
    # result = ", ".join(my_list)
    if artists_genres is not None:
        list_artists_genres.append(", ".join(artists_genres))
    else:
        list_artists_genres.append(None)

print(list_artists_genres)

artists_info = pd.DataFrame(
    {
        artist_id: artist_id, 
        artist_name: artist_name, 
        artists_genres: list_artists_genres}
)

print(artists_info)
