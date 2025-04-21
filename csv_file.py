from getting_recently_played_songs import getting_recently_played_tracks
import pandas as pd

def create_csv_file(track_list):
    df = pd.DataFrame(track_list)
    df.to_csv('spotify_tracking.csv', index=False)

def read_csv_file():
    df = pd.read_csv('spotify_tracking.csv')
    return df

