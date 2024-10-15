import numpy as np
import pandas as pd

def fetch(df, Year, Country):
    # Remove duplicate rows based on key columns
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    duplicate_mask = medal_df.columns.duplicated()

    # Keep only the columns that are not duplicated
    medal_df = medal_df.loc[:, ~duplicate_mask]
    flag = 0
    
    # Convert Year to integer if not 'OverAll'
    if Year != 'OverAll':
        Year = int(Year)  # Ensure Year is an integer

    # Handle the filtering conditions
    if Year == 'OverAll' and Country == 'OverAll':
        Fetch_df = medal_df
    elif Year == 'OverAll' and Country != 'OverAll':
        flag = 1
        Fetch_df = medal_df[medal_df['region'].str.lower() == Country.lower()]  # Normalize casing
    elif Year != 'OverAll' and Country == 'OverAll':
        Fetch_df = medal_df[medal_df['Year'] == Year]
    elif Year != 'OverAll' and Country != 'OverAll':
        Fetch_df = medal_df[(medal_df['Year'] == Year) & (medal_df['region'].str.lower() == Country.lower())]

    # Check if Fetch_df is empty
    if Fetch_df.empty:
        return pd.DataFrame({'Error': [f"No data found for Year: {Year}, Country: {Country}"]})

    # Grouping and summing the medals
    if flag == 1:
        x = Fetch_df.groupby('Year').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = Fetch_df.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    # Adding the total medal count (this part caused the error)
    # Sum row-wise across 'Gold', 'Silver', 'Bronze'
    x['total'] = x[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum(numeric_only=True)[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally

def country_year_list(df):
    Years = df['Year'].unique().tolist()
    Years.sort()
    Years.insert(0, 'OverAll')
    
    Country = np.unique(df['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0, 'OverAll')  # Use consistent case

    return Years, Country

def data_over_time(df , col):

    nations_over_time = df.drop_duplicates(['Year' , col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Editions' , 'count':col} , inplace=True)

    return nations_over_time


# Define the most_successful function
def most_successful(df, sport):
    # Filter out rows where 'Medal' is NaN (considering only athletes who won medals)
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'OverAll':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Get the top 15 athletes based on medal count
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge back to get additional details
    x = medal_counts.head(15).merge(temp_df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']]
    
    return x.drop_duplicates('Name')  # Drop duplicates if any

def year_wise_medal(df , country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team' , 'NOC' , 'Games' , 'Year' , 'City' , 'Sport' , 'Event' , 'Medal'] , inplace = True)

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
    # Filter the DataFrame for the selected country and for athletes who won a medal
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 10 athletes by medal count
    medal_counts = temp_df['Name'].value_counts().reset_index().head(10)
    medal_counts.columns = ['Name', 'Medals']  # Rename columns for clarity

    # Merge the top 10 medalists with the original DataFrame to get additional details
    x = medal_counts.merge(temp_df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
    
    return x


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final