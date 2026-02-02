import pandas as pd

def initial_analysis(df):
    print(f'NUMBER OF TRACKS LISTENED: {len(df)}')

def streaming_per_year(df):    
    # Counting number of rows per year
    rows_per_year = df['played_at'].dt.to_period('Y').value_counts().sort_index()
    print(rows_per_year)

def streamings_per_month(df):
    # Counting number of rows per month
    rows_per_month = df['played_at'].dt.to_period('M').value_counts().sort_index()
    print(rows_per_month)

def streamings_per_day(df):
    # Counting number of rows per day
    rows_per_hour = df['played_at'].dt.to_period('D').value_counts()
    print(rows_per_hour)

def minutes_streamed_in_general(df):
    return df['duration_ms'].sum() / 60000

def ms_to_minutes(milliseconds):
    return milliseconds / 60000

def minutes_streamed_per_year(df):
    return df.groupby(
        df['played_at'].dt.to_period('Y')
    )['duration_ms'].sum().apply(ms_to_minutes)

def minutes_streamed_per_month(df):
    return df.groupby(
        df['played_at'].dt.to_period('M')
    )['duration_ms'].sum().apply(ms_to_minutes)
