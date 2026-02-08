import pandas as pd
import ast

def reading_genres_file():
    df = pd.read_csv('data/artists_genres.csv').drop_duplicates().dropna()
    df = df.rename(columns={'id': 'artist_id'})
    return df
def reading_tracking_file():
    return pd.read_csv('data/spotify_tracking.csv')

def get_artists_genres():
    df = reading_genres_file()
    new_genres_list = []

    for row in df.itertuples():
        # print('\n',row.genres)
        for genre in row.genres.split(', '):
            # print(f'#{genre}')
            new_genres_list.append(
                {
                    'artist_id': row.artist_id,
                    'genre': genre
                }
            )

    return pd.DataFrame(new_genres_list)

def adding_genre_column():
    df_tracking = reading_tracking_file()
    df_genres = reading_genres_file()

    df_tracking["artist_ids_list"] = df_tracking["artist_id"].apply(ast.literal_eval)
    tracking_exploded = df_tracking.explode("artist_ids_list")
    
    tracking_with_genres = tracking_exploded.merge(
        df_genres,
        left_on="artist_ids_list",
        right_on="artist_id",
        how="left"
    )


    # print(df_tracking["artist_ids_list"], df_genres)
    # genres_join = df_tracking.merge(df_genres, on='artist_id')
    print(tracking_with_genres)
    tracking_with_genres.to_csv('test_genres.csv')

adding_genre_column()

# def songs_per_genre():
#     df = get_artists_genres()
#     return df['genre'].value_counts()

# print(songs_per_genre())