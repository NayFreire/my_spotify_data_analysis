from spotify_credentials import get_sp_credentials

sp = get_sp_credentials()

# Ex: looking for an artist
result = sp.search(q='Arctic Monkeys', type='artist')
artist = result['artists']['items'][0]

print(f"Name: {artist['name']}")
print(f"Popularidade: {artist['popularity']}")
print(f"Gêneros: {artist['genres']}")