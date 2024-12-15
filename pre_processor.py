import pandas as pd

def preprocessing():
    # Load datasets
    df = pd.read_csv('./data/athlete_events.csv')
    region_df = pd.read_csv('./data/noc_regions.csv')
    
    # Filter Summer Olympics data
    df = df[df["Season"] == "Summer"]
    
    # Merge with region data
    df = df.merge(region_df, on='NOC', how='left')
    
    # Remove duplicate entries
    df.drop_duplicates(inplace=True)
    
    # One-hot encoding for Medal column
    medal_dummies = pd.get_dummies(df['Medal'], prefix='Medal')
    df = pd.concat([df, medal_dummies], axis=1)
    
    return df
