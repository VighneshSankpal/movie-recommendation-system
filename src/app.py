
import streamlit as st
import requests
import pandas as pd
import numpy as np
from utils.streamlit_functions import get_movie
from components.style import load_css,load_css_file
from components.utils import navitagor

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"  # Important
)


load_css_file('src/components/style.css')
load_css()
# tmdb_movieId and moviePosterPath mapping

movie_posterPath = pd.read_csv('dataset/processed/movieId_poster.csv')
movieId_lookup = pd.read_csv('dataset/processed/movieId_lookup.csv')

# initialized movie session state:
if 'movie_show' not in st.session_state:
    st.session_state['movie_show'] = {
        'movie_title' : None,
        'movie_id' :None
    }

# Display movies
def movie_card(movie_id):

    poster_path  = movie_posterPath.loc[movie_posterPath['tmdb_movieId']==movie_id,'poster_path'].values[0]
    if poster_path == 'unknown':

        data = get_movie(movie_id)

        if data is None:
            return

        poster_path = data.get("poster_path")
        

        movie_posterPath.loc[movie_posterPath['tmdb_movieId']==movie_id,'poster_path'] = poster_path
        movie_posterPath.to_csv('dataset/processed/movieId_poster.csv',index=False)

    if poster_path:
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        st.image(poster_url, width=300)

    movie_title = movieId_lookup.loc[movieId_lookup['tmdb_movieId']== movie_id,['title_clean']].values[0,0]
    
    st.write(f'Title : {movie_title if len(movie_title) <18 else movie_title[:17]+'..'}')
    if st.button(label='Check Out it', key= f'movie-show-{movie_id}'):
        st.session_state['movie_show'] = {
        'movie_title' :movie_title,
        'movie_id' :movie_id
    }
        st.switch_page(page='pages/4_Movie_info.py')
    

st.markdown("""
<style>
.main .block-container {
    max-width: 100%;
    padding-top: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
    padding-bottom: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stMainBlockContainer"] {
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

with st.container(key="hero-container"):
    st.title("Welcome,")
    st.subheader('Millions of movies, TV shows and people to discover. Explore now.')

    # st.text_input(key='seach_bar', label='', placeholder='Seach for movie',label_visibility="collapsed",)
    
with st.container(key = 'free-container'):
    navitagor()


with st.container(key='explore-movie-container'):
    st.subheader("Explore Movies")

    movieId_layer1 = [14869, 131634, 11194, 64720, 137113]
    layer1_col = st.columns(5)
    for i in range(5):
        with layer1_col[i]:
            movie_card(movieId_layer1[i])


    movieId_layer2 = [68726, 411, 42684, 13937, 10439]
    layer2_col = st.columns(5)
    for i in range(5):
        with layer2_col[i]:
            movie_card(movieId_layer2[i])
