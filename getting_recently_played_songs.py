from spotify_credentials import get_sp_credentials

sp = get_sp_credentials()

# Getting the recently played songs
recent_tracks = sp.current_user_recently_played() # 50 is the max limit

recently_played_list = []

for item in recent_tracks['items']:
    track = item['track']
    track_info = {
        'id': track['id'],
        'name': track['name'],
        'artist_name': [artist['name'] for artist in track['artists']],
        'artist_id': [artist['id'] for artist in track['artists']],
        'release_date': track['album']['release_date'],
        'duration_ms': track['duration_ms'],
        'explicit': track['explicit'],
        'popularity': track['popularity'],
        'played_at': item['played_at']
    }
    # print(track_info, '\n')
    recently_played_list.append(track_info)
    
print(recently_played_list)
print(len(recent_tracks['items']))