import streamlit as st
import pre_processor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Preprocess data
df = pre_processor.preprocessing()

st.sidebar.title("Olympics Analysis")

# Sidebar options
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    
    # Get unique years and countries
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    
    # Fetch and display medal tally
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    
    # Dynamic title based on selection
    title = f"Medal Tally for {selected_country}" if selected_country != "Overall" else "Overall Medal Tally"
    if selected_year != "Overall":
        title += f" in {selected_year}"
    st.title(title)
    
    # Handle empty results
    if medal_tally.empty:
        st.write("No data available for the selected filters.")
    else:
        st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]  
    
    st.title("Top statistics")   

    # Create columns for the stats display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.title(editions)
    with col2:
        st.subheader("Cities")
        st.title(cities)
    with col3:
        st.subheader("Sports")
        st.title(sports)

    # Create new columns for remaining stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.title(events)
    with col2:
        st.subheader("Athletes")
        st.title(athletes)
    with col3:
        st.subheader("Nations")
        st.title(nations)

    # Fetch nations over time data
    nations_over_time = helper.count_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="Count", title="Participating Nations over the years")
    st.plotly_chart(fig)

    # Fetch events over time data
    event_over_time = helper.count_over_time(df, 'Event')
    
    # Plot using Plotly Express for events
    fig = px.line(event_over_time, x="Edition", y="Count", title="Events over the years")
    st.plotly_chart(fig)
    
    # Fetch athletes over time data
    athletes_over_time = helper.count_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Count", title="Athletes over the years")
    st.plotly_chart(fig)
    
    st.title('Number of Events over time (Every Sport)')
    fig, ax = plt.subplots(figsize=(20, 20))
    X = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(X.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0), annot=True)
    st.pyplot(fig)
    
    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    
    selected_sport = st.sidebar.selectbox("Select Sport", sport_list)
    successful_athletes = helper.most_successful(df, selected_sport)
    st.table(successful_athletes)


if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    
    # List of countries for the selection
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    
    # Medal tally over the years for the selected country
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)
    
    # Displaying the sports in which the country excels
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)
    
    # Selecting the country again to fetch the top 10 athletes
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)
