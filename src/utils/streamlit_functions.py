import streamlit as st
import requests
import pandas as pd
import os 

@st.cache_data(ttl=3600)
def get_movie(movie_id):

    API_KEY = st.secrets['TMDB_API_KEY']

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": API_KEY}

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        # st.error(f"Movie {movie_id}: {e}")
        st.text("Clould Not Load")
        return None
    except Exception as e:
        st.text("Clould Not Load")

    
@st.cache_data(ttl=3600)
def getMovie_lookup():
    try:
        file_path =        os.path.join('dataset','processed','movieId_lookup.csv')

        movieId_lookup =  pd.read_csv(file_path)

    except FileNotFoundError as e:
        st.write("Movie Lookup File Not Avaiable.. :< ")
        st.write(e)
        st.stop()

    return movieId_lookup
  

