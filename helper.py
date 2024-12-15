import numpy as np

# Function to fetch unique years and countries
def country_year_list(df):
    years = sorted(df['Year'].dropna().unique().tolist())
    years.insert(0, 'Overall')
    countries = sorted(df['region'].dropna().unique().tolist())
    countries.insert(0, 'Overall')
    return years, countries

# Function to fetch medal tally based on year and country
def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    
    # Apply filters
    if year == 'Overall' and country == "Overall":
        temp_df = medal_df
    elif year == 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    elif country == "Overall":
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    
    # Group by Year or Region
    if country != "Overall":
        grouped = temp_df.groupby('Year').sum(numeric_only=True)
    else:
        grouped = temp_df.groupby('region').sum(numeric_only=True)
    
    # Aggregate medal counts
    grouped = grouped[['Medal_Gold', 'Medal_Silver', 'Medal_Bronze']].sort_values('Medal_Gold', ascending=False).reset_index()
    grouped['Total'] = grouped['Medal_Gold'] + grouped['Medal_Silver'] + grouped['Medal_Bronze']
    
    # Rename columns for display
    grouped.rename(columns={
        'Medal_Gold': 'Gold',
        'Medal_Silver': 'Silver',
        'Medal_Bronze': 'Bronze'
    }, inplace=True)
    
    return grouped


def data_over_time(df, col):
    # Count the number of unique nations per year
    nations_over_time = df.groupby('Year')[col].nunique().reset_index()
    nations_over_time.rename(columns={'Year': 'Edition', col: 'Count'}, inplace=True)
    return nations_over_time

def event_over_time(df, col):
    # Count the number of unique nations per year
    nations_over_time = df.groupby('Year')[col].nunique().reset_index()
    nations_over_time.rename(columns={'Year': 'Edition', col: 'Count'}, inplace=True)
    return nations_over_time



