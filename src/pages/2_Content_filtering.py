import streamlit as st
from components.utils import setup_page
from utils.streamlit_functions import getMovie_lookup,get_movie



# ---------------------------------------------------------------------
# session state session




if  'movie_btn_click' not in st.session_state:
    st.session_state['movie_btn_click'] = False







# --------------------------------------------------------------------
# Intializing data
MOVIEID_LOOKUP =  getMovie_lookup()
all_movies = MOVIEID_LOOKUP['title_clean'].unique().tolist()
all_movies.sort()


# movie_details = funct_movie_detailes()
# try:
#     movie_details = get_movie()
# except Exception as e:
#     st.write("Movie is not accessible :(")
#     st.stop()

# if not movie_details:
#     st.write("Movie is not accessible :(")
#     st.stop()

# ---------------------------------------------------------------------
# Application Layout
setup_page()

with st.container():
    st.subheader("Content Filtering")

    # st.dataframe(MOVIEID_LOOKUP)

    st.subheader("Select your favorite movie")
    with st.container(key='movie_selection'):
        
        selected_movie = st.selectbox(label='Select Movie', options=all_movies[70:],placeholder='select movie',index=None,width=500)
        if st.button("Get Movie"):
            st.session_state['movie_btn_click'] = True
        


    if st.session_state['movie_btn_click']:
        st.write("You selected movie is ", selected_movie)
        try :
            movie_id = MOVIEID_LOOKUP.loc[MOVIEID_LOOKUP['title_clean']== selected_movie,'tmdb_movieId'].values[0]
        except IndexError as e:
            st.write("Select Movie")
            st.stop()

        try:
            movie_details = get_movie(movie_id)
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
