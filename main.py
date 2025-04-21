from getting_recently_played_songs import getting_recently_played_tracks
from csv_file import create_csv_file, read_csv_file
import pandas as pd
import os

#create_csv_file(current_track_list)

# Getting the list of recently played tracks and transforming into a dataframe
current_tracks_df = pd.DataFrame(getting_recently_played_tracks())

# Getting the dataframe from the csv file
track_list = read_csv_file()

# Creating a unique column to verify if there are new tracks to be added. It combines 'id' and 'played_at' so I can verify both values at the same time. Cause I need to verify if track X played at time Y is already added to the csv file.

current_tracks_df['id_played_at'] = current_tracks_df['id'] + current_tracks_df['played_at']
track_list['id_played_at'] = track_list['id'] + track_list['played_at']

# Getting the data not yet added to the csv file. 

new_data = current_tracks_df[~current_tracks_df['id_played_at'].isin(track_list['id_played_at'])]
print(new_data)

# Removing the 'id_played_at' column so the data can have the same format as the dataframe in the csv file
new_data = new_data.drop(columns=['id_played_at'], errors='ignore')

# Adding the new tracks to the csv file
new_data.to_csv('spotify_tracking.csv', mode='a', index=False, header=not os.path.exists('spotify_tracking.csv'))