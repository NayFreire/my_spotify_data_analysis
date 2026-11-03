import requests as req
import pandas as pd

lyrics_df = pd.DataFrame(pd.read_csv('data/lyrics.csv'))
no_lyrics_df = lyrics_df[lyrics_df['song_genius_id'].isna()]
# print(len(lyrics_df))
# print(no_lyrics_df)

base_url = 'https://lrclib.net'

for track in no_lyrics_df.itertuples():
    print(track)
    name = track.song_name.replace(' ', '+')
    artist = track.artist_name.replace(' ', '+')
    print((f'{base_url}/api/get?artist_name={artist}&track_name={name}'))
    response = req.get(f'{base_url}/api/get?artist_name={artist}&track_name={name}')
    print(response.content, '\n\n')