import streamlit as st
from utils.streamlit_functions import get_movie

from components.utils import setup_page
# initialized movie session state:
if 'movie_show' not in st.session_state:
    st.session_state['movie_show'] = {
        'movie_title' : None,
        'movie_id' :None
    }

setup_page()

# @st.cache_data 
# def funct_movie_detailes():
#     return get_movie(st.session_state['movie_show']['movie_id'])

# movie_details = funct_movie_detailes()
try:
    movie_details = get_movie(st.session_state['movie_show']['movie_id'])
except Exception as e:
    st.write("Movie is not accessible :(")
    st.stop()

if not movie_details:
    st.write("Movie is not accessible :(")
    st.stop()
    

with st.container():
    st.subheader("Movie Information")
    


    movie_poster_col, movie_details_col = st.columns(2)
    with movie_poster_col:
        with st.container(key='info_movie_poster'):
            poster_path = movie_details.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            st.image(poster_url, width=400)


    movie_genres = ', '.join([item['name'] for item in movie_details['genres']])
    with movie_details_col:

        st.html(
            f'''
            <div id='movie_inforamtion_section'>
            <h2>{movie_details['title']} </h2>
            <p>Releasted On : {movie_details['release_date']}</p>
            <span>Genres : {movie_genres}</span>
            </br>
        
            <i>{movie_details['tagline']}</i>
            <h4>Overview :</h4>
            <p id = 'overview_content'>{movie_details['overview']}</p>
            </div>
            '''
        )
st.json(movie_details)