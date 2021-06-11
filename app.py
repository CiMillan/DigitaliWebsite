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

#---------------------------------------------------------------#
# PAGE STRUCTURE
#---------------------------------------------------------------#
# Use the full page instead of a narrow central column

st.set_page_config(
    page_title="Hit Predictor",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed")

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

sidebar_options = st.sidebar.radio('What do you want to predict?', ('Movies', 'Series'))

SIDEBAR_FONT_SIZE_CSS = f"""
<style>
label {{
    font-size: 22px !important;
}}
</style>
"""
st.write(SIDEBAR_FONT_SIZE_CSS, unsafe_allow_html=True)

#---------------------------------------------------------------#
# DROPDOWN MOVIES
#---------------------------------------------------------------#
    
if sidebar_options == 'Get Score by Title':

    sorted_movies = data.groupby('original_title')['title'].count()\
        .sort_values(ascending=False).index

    st.markdown("### **Select Movie:**")
    select_movie = []

    select_movie.append(st.selectbox('', sorted_movies))

    #Filter df based on selection
    movie_df = data[data['original_title'].isin(select_movie)]

    # major_cluster = artist_df.groupby('clusters')['search_query'].count()\
    #     .sort_values(ascending = False).index[0]
    
    one_title_df = movie_df.groupby(['imdb_title_id'],as_index=False).agg(lambda x : x.mean() if x.dtype=='int64' else x.head(1))
    first_table = one_title_df[['year', 'genre', 'duration', 'country', 'actors', 'avg_vote', 'votes',
       'budget', 'worlwide_gross_income', 'metascore',
       'reviews_from_users', 'reviews_from_critics',]]
    first_table
    
    if len(first_table) < 2:
        if st.button('Reveal Score'):
            st.write('Score is ...')
    else:
        selected_indices = st.multiselect('Select rows:', first_table.index)
        
        if st.button('Reveal Score'):
            for i in range (0, len(selected_indices)):
                film = select_movie[0]
                year = first_table.iloc[i , 0]
                score = first_table.iloc[i , 5]
                st.write(f'The predicted score for the film {film} from {year} is {score}')
        
    
    
    
    # for i in range(0, len(first_table)):
    #     cols = st.beta_columns(6)
    #     cols[0].write(first_table['imdb_title_id'][i])
    #     cols[1].write(first_table['year'][i])
    #     cols[2].write(first_table['genre'][i])
    #     cols[3].write(first_table['country'][i])
    #     cols[4].write(first_table['duration'][i])
    #     cols[5].write(first_table['language'][i])
    
    for i in range(0, ):
        if st.button('find score'):
            st.write('Score is ...')

    
    with st.beta_expander("Select by feature"):
    
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
        if st.button('find score'):
            st.write('Score is ...')
    
    #col1, col2 = st.beta_columns(2)
    
    #with col1:
        #st.markdown(f"**Year:** {movie_df['year']}")
        #st.markdown(f"**Top Song:** " +\
                    #f"{movie_df.loc[movie_df['track_rank']==np.min(movie_df['track_rank']),'search_query'].values[0]}")
        
    # with col2:
    #     st.markdown(f"**Highest Rank:** {np.min(artist_df['track_rank'])}")
    #     st.markdown(f"**Major Cluster:** {major_cluster}")

#---------------------------------------------------------------#
# DROPDOWN SERIES
#---------------------------------------------------------------#
    
elif sidebar_options == 'Select a Ranking range':
    st.write('▶️')
    
    # sorted_movies = data.groupby('Title')['search_query'].count()\
    #     .sort_values(ascending=False).index

    # st.markdown("### **Select Movie:**")
    # select_movie = []

    # select_movie.append(st.selectbox('', sorted_movies))

    # #Filter df based on selection
    # movie_df = data[data['search_movie'].isin(select_movie)]

    # major_cluster = artist_df.groupby('clusters')['search_query'].count()\
    #     .sort_values(ascending = False).index[0]
    
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