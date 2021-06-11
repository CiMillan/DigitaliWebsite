import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from PIL import Image

#---------------------------------------------------------------#
# GET DATAFRAMES
#---------------------------------------------------------------#

data = pd.read_csv('raw_data/linear.csv')
#remove indexes
data = data.assign(hack='').set_index('hack')

#---------------------------------------------------------------#
# PAGE STRUCTURE
#---------------------------------------------------------------#
# Use the full page instead of a narrow central column

st.set_page_config(
    page_title="Hit Predictor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="auto") # or collapsed

image = Image.open('Digitalilogo.jpg')
st.sidebar.image(image)

st.markdown(f"""
    # Hit Predictor
    """)

TITLE_FONT_SIZE_CSS = f"""
<style>
h1 {{
    font-size: 42px !important;
}}
</style>
"""
st.write(TITLE_FONT_SIZE_CSS, unsafe_allow_html=True)

#---------------------------------------------------------------#
# SIDEBAR RADIO MOVIES OR SERIES
#---------------------------------------------------------------#

sidebar_options = st.sidebar.radio('Choose one option:', ('Get Score by Title', 'Select a Ranking Range', 'Sort by Features'))

SIDEBAR_FONT_SIZE_CSS = f"""
<style>
label {{
    font-size: 22px !important;
}}
</style>
"""
st.write(SIDEBAR_FONT_SIZE_CSS, unsafe_allow_html=True)

#---------------------------------------------------------------#
# DROPDOWN SCORE BY TITLE
#---------------------------------------------------------------#
    
if sidebar_options == 'Get Score by Title':

    sorted_movies = data.groupby('original_title')['title'].count()\
        .sort_values(ascending=False).index

    st.markdown("### **Select Movie:**")
    select_movie = []

    select_movie.append(st.selectbox('', sorted_movies))

    #Filter df based on selection
    movie_df = data[data['original_title'].isin(select_movie)]

    #Group by IMDb ID
    one_title_df = movie_df.groupby(['imdb_title_id'],as_index=False).agg(lambda x : x.mean() if x.dtype=='int64' else x.head(1))
    first_table = one_title_df[['year', 'genre', 'duration', 'country', 'avg_vote', 'votes', 'worlwide_gross_income',
       'reviews_from_users',]]
    st.table(first_table)
    
    #Score Button for only one result vs more results
    film1 = one_title_df['original_title'][0]
    score1 = first_table.iloc[0 , 5]
    if len(first_table) < 2:
        if st.button('Reveal Score'):
            st.write(f'The predicted score for the film **{film1}** is **{score1}**')
    else:
        selected_indices = st.multiselect('Select rows to compare:', first_table.index)
        if st.button('Reveal Score'):
            for i in range (0, len(selected_indices)):
                film2 = select_movie[0]
                year = first_table.iloc[i , 0]
                score2 = first_table.iloc[i , 5]
                st.write(f'The predicted score for the film **{film2}** from {year} is **{score2}**')
    
    #Expander to reveal more features of selected movie(s)
    with st.beta_expander("Disclose more features"):
    
        col1, col2, col3, col4, col5, col6 = st.beta_columns(6)
    
        with col1:
            st.subheader("IMDb ID")
        with col2:
            st.subheader("Year")
        with col3:
            st.subheader("Genre")
        with col4:
            st.subheader("Country")
        with col5:
            st.subheader("Duration")
        with col6:
            st.subheader("Language")
        
        if len(first_table) < 2:
                cols = st.beta_columns(6)
                cols[0].write(one_title_df['imdb_title_id'][0])
                cols[1].write(one_title_df['year'][0])
                cols[2].write(one_title_df['genre'][0])
                cols[3].write(one_title_df['country'][0])
                cols[4].write(one_title_df['duration'][0])
                cols[5].write(one_title_df['language'][0])
        else:  
            for i in range(0, len(selected_indices)):
                cols = st.beta_columns(6)
                cols[0].write(one_title_df['imdb_title_id'][i])
                cols[1].write(one_title_df['year'][i])
                cols[2].write(one_title_df['genre'][i])
                cols[3].write(one_title_df['country'][i])
                cols[4].write(one_title_df['duration'][i])
                cols[5].write(one_title_df['language'][i])

#---------------------------------------------------------------#
# DROPDOWN RANKING RANGE
#---------------------------------------------------------------#
    
elif sidebar_options == 'Select a Ranking Range':

    option = st.slider('Select the number of rows', 1, 50, 5)
    print(option) #prints on the terminal
    filtered_df = st.table(data[['original_title', 'year']].head(option))
    
#---------------------------------------------------------------#
# DROPDOWN SORT FEATURES
#---------------------------------------------------------------#
    
elif sidebar_options == 'Sort by Features':
    
    col1, col2, col3, col4, col5, col6 = st.beta_columns(6)
    
    with col1:
        d = list(data['year'].drop_duplicates())
        d.insert(0, "-")
        year = st.selectbox("Year", d)
    with col2:
        g = list(data['genre'].drop_duplicates())
        g.insert(0, "-")
        genre = st.selectbox("Genre", g)
    # with col3:
    #     country = st.selectbox("Country", data['country'].drop_duplicates())
    # with col4:
    #     avg_votes = st.selectbox("Avg Votes", data['avg_vote'].drop_duplicates().sort_values(ascending=False))
    # with col5:
    #     budget = st.selectbox("Budget", data['budget'].drop_duplicates().sort_values(ascending=False))
    # with col6:
    #     income = st.selectbox("Income", data['worlwide_gross_income'].drop_duplicates().sort_values(ascending=False))
    
    
    fields = ['year', 'genre']
    inputs = [year, genre]#, country, avg_votes, budget, income]
    
    field_dict = {}
    for index, input in enumerate(inputs):
        if input != "-":
            field_dict[fields[index]] = input
    
    test = data.copy()
    
    for key, value in field_dict.items():
        print(key, value)
        test = test[test[key] == value]
    
    if test.empty:
        st.write('No results for your query')
    else:
        test        






else:
    st.write('◀️')
    
#---------------------------------------------------------------#
# API
#---------------------------------------------------------------#

# title = st.text_input("Title", "The Crown")

# country_origin = st.text_input("Country of origin", "UK")
# genre = st.text_input("Genre", "Drama")
# total_predictions = st.slider('Number of Titles', 1, 20, 1)

# url = 'https://taxifare.lewagon.ai/predict'

# params = {
#     "title": title,
#     "country_origin": country_origin,
#     "genre": genre,
#     "total_predictions": total_predictions
# }

# response = requests.get(url=url, params=params).json()
# prediction = round(response['prediction'], 2)

# st.write(f"**There's a {prediction} likelihood of {title} being a hit**")