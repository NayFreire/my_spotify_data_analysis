from getting_recently_played_songs import getting_recently_played_tracks
from csv_file import create_csv_file, read_csv_file
import pandas as pd
import os

current_tracks_df = pd.DataFrame(getting_recently_played_tracks())
# create_csv_file(current_track_list)

track_list = read_csv_file()
print(track_list)
print(current_tracks_df)

current_tracks_df['id_played_at'] = current_tracks_df['id'] + current_tracks_df['played_at']

track_list['id_played_at'] = track_list['id'] + track_list['played_at']

new_data = current_tracks_df[~current_tracks_df['id_played_at'].isin(track_list['id_played_at'])]

print(new_data)

new_data = new_data.drop(columns=['id_played_at'], errors='ignore')

new_data.to_csv('spotify_tracking.csv', mode='a', index=False, header=not os.path.exists('spotify_tracking.csv'))