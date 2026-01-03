from getting_recently_played_songs import getting_recently_played_tracks
from csv_file import create_csv_file, read_csv_file
from getting_genres import getting_artists_genres
from getting_albums import getting_tracks_albums
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
print('NEW DATA:\n', new_data)

# Removing the 'id_played_at' column so the data can have the same format as the dataframe in the csv file
new_data = new_data.drop(columns=['id_played_at'], errors='ignore')

if len(new_data) > 0:
    # Adding the new tracks to the csv file
    #TODO: Create a function to verify if the new tracks are also available 

    genres = pd.DataFrame(pd.read_csv('data/artists.csv'))
    albums = pd.DataFrame(pd.read_csv('data/tracks.csv'))

    # Iterating through the new data, to verify if the track and artist on it have already been inserted in their csv files

    for track in new_data.itertuples():
        # Verifying if the track and artist are already in the files
        artist_already_cataloged = genres['id'].isin(track.artist_id).any()
        track_already_cataloged = albums['track_id'].isin([track.id]).any()

        # If they are not, they need to be added
        if not artist_already_cataloged:
            artist_info = getting_artists_genres([track.artist_id]) # getting api data to add
            artist_info = pd.DataFrame(artist_info)
            artist_info.to_csv('data/artists.csv', mode='a', index=False, header=not os.path.exists('data/artists.csv')) # adding data to the file
        if not track_already_cataloged:
            track_info = getting_tracks_albums([[track.id]]) # getting api data to add. The '[[track_id]]' is there, cause different from artists_id, the track id is just a string and 'getting_tracks_albums(id)' asks for a list. The other [] is for the for loop inside the function
            track_info = pd.DataFrame(track_info)
            track_info.to_csv('data/tracks.csv', mode='a', index=False, header=not os.path.exists('data/tracks.csv')) # adding data to the file

    new_data.to_csv('data/spotify_tracking.csv', mode='a', index=False, header=not os.path.exists('data/spotify_tracking.csv'))