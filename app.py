import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper
import plotly.express as px
import plotly.figure_factory as ff

st.sidebar.title('Olympics Data Analysis')
st.sidebar.image('download.jpeg')

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise analysis')
)

#st.dataframe(df)

################################################################################################

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.year_country_list(df)

    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Year',country)

    medal_tally  = helper.fetch_medal_tally(df,selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

####################################################################################################


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1 
    cities  = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]


    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Total Editions')
        st.title(editions)

    with col2:
        st.header('Hosting cities')
        st.title(cities)
    with  col3:
        st.header('Total Sports')
        st.title(sports)

    col1, col2,col3 = st.columns(3)

    with col1:
        st.header('Total Events')
        st.title(events)

    with col2:
        st.header('Total Atheletes')
        st.title(athletes)

    with col3:
        st.header('Participating Nations')
        st.title(nations)


    nations_over_time = df.drop_duplicates(subset=['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'count':'Number of participating countries'}, inplace= True)
    fig = px.line(nations_over_time, x = 'Year', y ='Number of participating countries')
    st.title('Participating Countries Over the Years')
    st.plotly_chart(fig)


    num_of_events_overtime = df.drop_duplicates(subset=['Year','Event'])['Year'].value_counts().reset_index().sort_values('Year')
    num_of_events_overtime.rename(columns={'count':'Number of Events'},inplace=True)
    fig = px.line(num_of_events_overtime, x = 'Year', y ='Number of Events')  
    st.title('Number of Events Over the Time')   
    st.plotly_chart(fig)


    num_of_athletes_overtime = df.drop_duplicates(subset=['Year','Name'])['Year'].value_counts().reset_index().sort_values('Year')
    num_of_athletes_overtime.rename(columns={'count':'Number of Athletes'},inplace=True)
    fig = px.line(num_of_athletes_overtime, x = 'Year', y ='Number of Athletes')  
    st.title('Number of Athletes Over the Time')   
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,axes = plt.subplots(figsize=(10,15))
    x = df.drop_duplicates(['Year','Sport','Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns= 'Year', values= 'Event', aggfunc= 'count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.title("Most successful Athletes")
    sport_list = x['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful_athelete(df,selected_sport)
    st.table(x)

###################################################################################

if user_menu == 'Country-wise Analysis':
      st.sidebar.title('Country-wise Analysis')

      country_list = df['region'].dropna().unique().tolist()
      country_list.sort()

      selected_country = st.sidebar.selectbox('Select a Country',country_list)

      country_df = helper.country_wise_medal_tally(df,selected_country)
      fig = px.line(country_df, x="Year", y="Medal")
      st.title(selected_country + " Medal Tally over the years")
      st.plotly_chart(fig)

      st.title(selected_country + " excels in the following sports")
      pt = helper.country_sport_heatmap(df,selected_country)
      fig, ax = plt.subplots(figsize=(10, 15))
      ax = sns.heatmap(pt,annot=True)
      st.pyplot(fig)

      st.title("Top 10 athletes of " + selected_country)
      top10_df = helper.top_10_athelete(df,selected_country)
      st.table(top10_df)


###################################################################################

if user_menu == 'Athlete wise analysis':
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



    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

       






