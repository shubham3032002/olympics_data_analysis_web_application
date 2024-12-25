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

# Combined function to count unique values over time (for nations and events)
def count_over_time(df, col):
    # Count the number of unique values (nations or events) per year
    count_over_time = df.groupby('Year')[col].nunique().reset_index()
    count_over_time.rename(columns={'Year': 'Edition', col: 'Count'}, inplace=True)
    return count_over_time

def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Get the top 15 athletes by medal count
    athlete_counts = temp_df['Name'].value_counts().reset_index()
    athlete_counts.columns = ['Name', 'Medal_Count']  # Rename columns for clarity
    athlete_counts = athlete_counts.head(15)

    # Merge to get more athlete details (e.g., Sport and Region)
    top_athletes = athlete_counts.merge(df, on='Name', how='left')[['Name', 'Medal_Count', 'Sport', 'region']].drop_duplicates('Name')

    return top_athletes

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df



def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt



def most_successful_countrywise(df, country):
    # Filter out rows with missing medal values
    temp_df = df.dropna(subset=['Medal'])

    # Filter for the selected country
    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 10 athletes by medal count
    athlete_counts = temp_df['Name'].value_counts().reset_index()
    athlete_counts.columns = ['Name', 'Medal_Count']  # Rename columns for clarity
    athlete_counts = athlete_counts.head(10)

    # Merge with the original DataFrame to get more details like Sport
    top_athletes = athlete_counts.merge(df, on='Name', how='left')[['Name', 'Medal_Count', 'Sport']].drop_duplicates('Name')

    return top_athletes