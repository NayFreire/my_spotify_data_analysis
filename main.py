import pandas as pd
from creating_data.csv_file import read_csv_file
from datetime import datetime, timedelta

df = pd.DataFrame(read_csv_file())
print(df.info())

def remove_hours(dtime):
    # Removing the 3 hours added by the Spotify API
    new_played_at = dtime - timedelta(hours=3)
    print(f"{dtime} -> {new_played_at}")
    return new_played_at

def correcting_played_at_column(df):
    # Converting 'played_at' from string to datetime
    df['played_at'] = pd.to_datetime(df['played_at'], format='ISO8601')

    # Applying the function 'remove_hours' to the column
    df['played_at'].apply(remove_hours)
    return df

# Fixing the 'played_at' column, 'cause the timestamp showed +3 hours
df = correcting_played_at_column(df)

# Sorting dataframe by values in 'played_at'
df = df.sort_values(by='played_at')
print(df)