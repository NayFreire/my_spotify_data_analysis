import pandas as pd
from datetime import datetime, timedelta

def remove_hours(dtime):
    # Removing the 3 hours added by the Spotify API
    new_played_at = dtime - timedelta(hours=3)
    
    return new_played_at

def correcting_played_at_column(df):
    # Converting 'played_at' from string to datetime
    df['played_at'] = pd.to_datetime(df['played_at'], format='ISO8601')

    # Applying the function 'remove_hours' to the column
    df['played_at'] = df['played_at'].apply(remove_hours)
    return df