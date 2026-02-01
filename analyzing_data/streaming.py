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