import streamlit as st
import pre_processor
import helper
import plotly.express as px

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
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="Count", title="Participating Nations over the years")
    st.plotly_chart(fig)

    # Fetch event over time data
    event_over_time = helper.event_over_time(df, 'Event')
    
    # Plot using Plotly Express for events
    fig = px.line(event_over_time, x="Edition", y="Count", title="Events over the years")
    st.plotly_chart(fig)
