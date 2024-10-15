import streamlit as st
import pandas as pd
import numpy as np
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


# Load the datasets
df = pd.read_csv('athlete_events.csv')
r_df = pd.read_csv('noc_regions.csv')

# Preprocess the data
df = preprocessor.preprocess(df, r_df)

# Sidebar title
st.sidebar.title('Olympic Analysis')

st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

# User menu options

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis')
)

# If user selects 'Medal Tally'
if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    Years, Country = helper.country_year_list(df)

    # Sidebar for Year and Country selection
    Selected_Year = st.sidebar.selectbox('Select Year', Years)
    Selected_Country = st.sidebar.selectbox('Select Country', Country)

    # Fetch medal tally based on user selection
    medal_tally = helper.fetch(df, Selected_Year, Selected_Country)

    # Display titles based on selection
    if Selected_Year == 'OverAll' and Selected_Country == 'OverAll':
        st.title('Overall Medal Tally')
    elif Selected_Year == 'OverAll' and Selected_Country != 'OverAll':
        st.title(f'Overall Performance of {Selected_Country}')
    elif Selected_Year != 'OverAll' and Selected_Country == 'OverAll':
        st.title(f'Medal Tally in {Selected_Year}')
    elif Selected_Year != 'OverAll' and Selected_Country != 'OverAll':
        st.title(f'Performance of {Selected_Country} in {Selected_Year}')

    # Display the medal tally DataFrame
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1   #No of the editions
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athlete = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1 , col2 , col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athlete)
    
    nations_over_time = helper.data_over_time(df , 'region')
    fig = px.line(nations_over_time , x="Editions" , y = "region")
    st.title("Participating Nations Over Years")
    st.plotly_chart(fig)

    # Correct line for plotting events over time
    events_over_time = helper.data_over_time(df, 'Event')

# Now use 'events_over_time' instead of 'nations_over_time'
    fig = px.line(events_over_time, x="Editions", y="Event")
    st.title("Events Over Years")
    st.plotly_chart(fig)

    Athelete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(Athelete_over_time, x="Editions", y="Name")  # Correct DataFrame here
    st.title("Total Participating Athletes Over Time")
    st.plotly_chart(fig)

    st.title("No of Events Over Time (Every Sport)")
    fig , ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year' , 'Sport' , 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport' , columns = 'Year' , values = 'Event' , aggfunc='count').fillna(0).astype('int'),
                    annot=True)
    st.pyplot(fig)


    st.title("Most Succesful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0 , 'OverAll')

    selected_sport = st.selectbox('Select a Sport' , sport_list)
    x = helper.most_successful(df , selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':
    
    st.sidebar. title('Country Wise Analysis')

    country_list = df['region'].unique().astype(str).tolist()
    country_list.sort()
    Selected_Country = st.sidebar.selectbox('Select a Country' , country_list)

    country_df = helper.year_wise_medal(df, Selected_Country)
    fig = px.line(country_df , x="Year" , y = "Medal")
    st.title(Selected_Country+" Medal Tally Over the Years")
    st.plotly_chart(fig)

    st.title(Selected_Country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,Selected_Country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + Selected_Country)
    top10_df = helper.most_successful_countrywise(df,Selected_Country)
    st.table(top10_df)

if user_menu == 'Athlete Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)




