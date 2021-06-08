import streamlit as st
import pandas as pd
import numpy as np
import requests

'''
# Hit Predictor
'''

title = st.text_input("Title", "The Crown")

country_origin = st.text_input("Country of origin", "UK")
genre = st.text_input("Genre", "Drama")
total_predictions = st.slider('Number of Titles', 1, 20, 1)


url = 'https://taxifare.lewagon.ai/predict'

params = {
    "title": title,
    "country_origin": country_origin,
    "genre": genre,
    "total_predictions": total_predictions
}

response = requests.get(url=url, params=params).json()
prediction = round(response['prediction'], 2)

st.write(f"**There's a {prediction} likelihood of {title} being a hit**")