import streamlit as st
from components.utils import setup_page
from utils.streamlit_functions import getMovie_lookup,get_movie

from utils.recommendation_method import get_movies_content_based
import pandas as pd
# ---------------------------------------------------------------------
# session state session



if  'movie_btn_click' not in st.session_state:
    st.session_state['movie_btn_click'] = False


if 'movie_id' not in st.session_state:
    st.session_state['movie_id'] = None




# --------------------------------------------------------------------
# Intializing data
MOVIEID_LOOKUP =  getMovie_lookup()
all_movies = MOVIEID_LOOKUP['title_clean'].unique().tolist()
all_movies.sort()

# movie poster url mapping file
movie_posterPath = pd.read_csv('dataset/processed/movieId_poster.csv')


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
# function defined
def movie_card(rm):
    with st.container(border=True):
        poster_path  = movie_posterPath.loc[movie_posterPath['tmdb_movieId']==rm.movie_id,'poster_path'].values[0]

        if poster_path == 'unknown':

            data = get_movie(rm.movie_id)

            if data is None:
                return

            poster_path = data.get("poster_path")
            

            movie_posterPath.loc[movie_posterPath['tmdb_movieId']==rm.movie_id,'poster_path'] = poster_path
            movie_posterPath.to_csv('dataset/processed/movieId_poster.csv',index=False)
        

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

            st.image(poster_url, width=300)

        
        movie_title = rm.movie_title
        
        # st.write(f'Movie Title is : {rm.movie_title}')
        # st.write(f'Movie_id is : {rmc.movie_id}')
    

        if rm.matching_keywords:
            similar_keywords = ', '.join(rm.matching_keywords)
            st.write(f'Matching Keywords are : {similar_keywords}')


        if rm.matching_gernes:
            similar_genres = ', '.join(rm.matching_gernes)
            st.write(f'Matching genres are : {similar_genres}')

        matching_plot = float(rm.overview_similarity)
        st.write(f'Plot similarity is : ')
        st.progress(value=round(matching_plot))
        st.write(f'{round(matching_plot,2)}% ')

        if rm.matching_director:

            st.write(f'Same movie Director.')


        
        # st.write(f'Title : {movie_title if len(movie_title) <18 else movie_title[:17]+'..'}')
        if st.button(label='Check Out it', key= f'movie-show-{rm.movie_id}'):
            st.session_state['movie_show'] = {
            'movie_title' :movie_title,
            'movie_id' :movie_id
        }
            st.switch_page(page='pages/4_Movie_info.py')




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
            st.session_state['movie_id'] = movie_id
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

    if  st.session_state['movie_id']:
        recommended_movies_info =   get_movies_content_based( st.session_state['movie_id'])

        
       
        with st.container(key='explore-movie-container'):
            st.subheader("Explore Movies")

            # Movies 1-5 showing
            with st.container(key='rm-content-lay1-container'):
                layer1_col = st.columns(5)
                for i in range(5):
                    with layer1_col[i]:
                        movie_card(recommended_movies_info[i])


            # Movies 6-10 showing
            with st.container(key='rm-content-lay2-container'):
                layer2_col = st.columns(5)
                for i in range(5):
                    with layer2_col[i]:
                        movie_card(recommended_movies_info[5:][i])
            

        for rmc in recommended_movies_info:
            st.write(f'Movie Title is : {rmc.movie_title}')
            st.write(f'Movie_id is : {rmc.movie_id}')
            st.write(f'Movie matching_keywords is : {rmc.matching_keywords}')
            st.write(f'Movie matching_gernes is : {rmc.matching_gernes}')
            st.write(f'Movie overview_similarity is : {rmc.overview_similarity}')
            st.write(f'Movie matching_director is : {rmc.matching_director}')
            st.write('-'*25)
        # st.json(movie_details)
