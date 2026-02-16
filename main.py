import pandas as pd
from creating_data.csv_file import read_csv_file
from analyzing_data.streaming import *
from analyzing_data.genres import *
from utils import correcting_played_at_column

df = pd.DataFrame(read_csv_file())
print(df.info())

# Fixing the 'played_at' column, 'cause the timestamp showed +3 hours
df = correcting_played_at_column(df)

# Sorting dataframe by values in 'played_at'
df = df.sort_values(by='played_at')
print(df)

initial_analysis(df)
# streamings_per_month(df)
# streaming_per_year(df)
# streamings_per_day(df)
print(f'Minutes streamed: {minutes_streamed_in_general(df)}')
print(f'Minutes streamed per year: {minutes_streamed_per_year(df)}')
print(f'Minutes streamed per month: {minutes_streamed_per_month(df)}')


df_with_genres = adding_genre_column()
all_genres, genres_grouped = getting_genres_numbers(df_with_genres)

top_5_genres = genres_grouped[1:6] # 1:6 is used to remove "other genres", because it's in the first position

# TODO: Get genres per year
top_genres_per_year = getting_genres_numbers_per_year(df_with_genres, 2025)