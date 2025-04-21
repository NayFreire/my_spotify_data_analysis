from spotify_credentials import getting_spotify_credentials

sp = getting_spotify_credentials()

# Ex: looking for an artist
result = sp.search(q='Arctic Monkeys', type='artist')
artist = result['artists']['items'][0]
print(f"Name: {artist['name']}")
print(f"Popularidade: {artist['popularity']}")
print(f"Gêneros: {artist['genres']}")