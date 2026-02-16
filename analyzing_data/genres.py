import pandas as pd
import ast

def reading_genres_file():
    df = pd.read_csv('data/artists_genres.csv').drop_duplicates().dropna()
    df = df.rename(columns={'id': 'artist_id'})
    return df

def reading_tracking_file():
    return pd.read_csv('data/spotify_tracking.csv')

def genres_string_to_list(genres):
    return genres.split(', ')

def adding_genre_column():
    # Getting the tracking dataframe and the genres one
    df_tracking = reading_tracking_file()
    df_genres = reading_genres_file()

    # The column artist_id is a list that was turned into a string once the dataframe was created. I need to tur it into a list again and put it into a new column
    df_tracking["artist_ids_list"] = df_tracking["artist_id"].apply(ast.literal_eval)

    # Exploding the artist_ids_list, means that I'm getting the list of IDs and separating them into different rows in the data frame. Therefore, if the list is ['a1', 'a2'], the df will now have 2 rows, one with the artist 1's id the another with the artist 2's id.
    tracking_exploded = df_tracking.explode("artist_ids_list")

    # Using 'merge' to bring the genres into the new dataframe
    tracking_with_genres = tracking_exploded.merge(
        df_genres, # the df where I want to get the info from
        left_on="artist_ids_list", # the column that will be user as primary key
        right_on="artist_id", # the column that will be used as foreign key (from the genres df)
        how="left" # the type of JOIN
    )

    # In the genres df, there are lots of rows with NaN values, for not all artists have genres on their spotify profile, so we need to drop them
    tracking_with_genres = tracking_with_genres.dropna()

    # Creating a new column and having it contain the genres as a list, instead of a string
    tracking_with_genres['unique_genres'] = tracking_with_genres['genres'].apply(genres_string_to_list)

    # Exploding the 'unique_genres' column, so that each row has only one genre
    genres_exploded = tracking_with_genres.explode('unique_genres')

    print(genres_exploded)

    # Creating a .csv file with the created df
    # genres_exploded.to_csv('test_genres.csv')
    return genres_exploded

def getting_genres_data(df):
    # Number of genres listened
    number_of_genres = len(df['unique_genres'].value_counts())
    print(number_of_genres)

    # Genres listened
    genres = df['unique_genres'].value_counts()
    # print(genres)

    # Grouping rare genres into the "other genres" category

    min_count = 100 # Number of minimum rows in the df

    mask = genres < min_count # Mask verifies if the corresponding genres shows up less times than the minimum count

    genres_grouped = (
        genres
        .rename(index=lambda genre: "other genres" if mask.get(genre, False) else genre) # Verifying if a genre's count is lower than the minimum count. If true, the genre is renamed "other genres". If false, the genre keep its name
        .groupby(level=0) # Grouping by the index on level 0, which is 'unique_genres'
        .sum() # Sum all the genres' counts. This makes it so, all the genres renamed "other genres" will become one with all its counts summed
    )

    genres_grouped = genres_grouped.sort_values(ascending=False) # Sorting the counts from biggest value to smallest

    print(genres_grouped)

    return genres_grouped

df_with_genres = adding_genre_column()
genres = getting_genres_data(df_with_genres)
top_5_genres = genres[1:6] # 1:6 is used to remove 'other genres' 