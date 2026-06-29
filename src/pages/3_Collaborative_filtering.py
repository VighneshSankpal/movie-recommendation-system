import streamlit as st

from components.utils import setup_page
import pandas as pd
import numpy as np
import json
from utils.recommendation_method import collaborative_based_filtering
from utils.streamlit_functions import getMovie_lookup,get_movie

# Page setup-config and navigation part.
setup_page()

# -------------------------------------------------------
# session state 
if 'userId' not in st.session_state:
    st.session_state['userId'] = None

# ------------------------------------------------------


# function defination
@st.cache_data(ttl=336)
def get_users_data():
    try:
        with open('dataset/processed/user_movies_historical_data_clean.json','r') as file:
            user_data = json.load(file) 
            return user_data
    except FileNotFoundError as e:
        st.write("User data not found.")
        return None

import streamlit as st

def show_user_profile(user):
    with st.container(border=True):

        col1, col2 = st.columns([1, 5])

        with col1:
            st.markdown("# 👤")

        with col2:
            st.subheader(f"User #{user['user_id']}")
            st.metric(
                "Average Rating Given",
                f"{user['average_rating']:.2f}/5"
            )

        st.divider()

        st.markdown("### 🎭 Favorite Genres")

        genre_cols = st.columns(len(user["top_genres"]))

        for col, genre in zip(genre_cols, user["top_genres"]):
            with col:
                st.success(genre)

        st.divider()

        st.markdown("### ❤️ Favorite Movies")

        movie_cols = st.columns(2)

        left = user["favorite_movies"][:5]
        right = user["favorite_movies"][5:]

        with movie_cols[0]:
            for movie in left:
                st.write(f"• {movie}")

        with movie_cols[1]:
            for movie in right:
                st.write(f"• {movie}")


def movie_card(rm):
    with st.container(border=True):
    
        tmdb_movieId =  movieId_lookup.loc[movieId_lookup['movieLens_movieId']==rm['movieId'],'tmdb_movieId'].values[0]
        poster_path  = movie_posterPath.loc[movie_posterPath['tmdb_movieId']==tmdb_movieId,'poster_path'].values[0]
        if poster_path == 'unknown':

            data = get_movie(tmdb_movieId)

            if data is None:
                return

            poster_path = data.get("poster_path")
            

            movie_posterPath.loc[movie_posterPath['tmdb_movieId']==tmdb_movieId,'poster_path'] = poster_path
            movie_posterPath.to_csv('dataset/processed/movieId_poster.csv',index=False)
        

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

            st.image(poster_url, width=300)
        
        
        movie_title = str(rm['title'])


             
        st.markdown(
            f"""
            <div style="
                height: 60px;
                font-size: 1.4rem;
                font-weight: 600;
                line-height: 1.3;
                overflow: hidden;
            ">
                {movie_title}
            </div>
            """,
            unsafe_allow_html=True,
        )
        predicted_rating = rm["predicted_rating"]

        score = ((predicted_rating - 0.5) / 4.5) * 100
        score = max(0, min(100, score))  # Clamp to 0–100

        st.caption(f"Predicted Rating: ⭐ {predicted_rating:.2f}/5")
        st.caption(f"Recommendation Score: {score:.1f}%")
        st.progress(int(score))
    

# -------------------------------------------------------
# variable initialization
users_data = get_users_data()
movieId_lookup = getMovie_lookup()

# movie poster url mapping file
movie_posterPath = pd.read_csv('dataset/processed/movieId_poster.csv')

# {'title': 'Hoop dreams', 'predicted_rating': np.float64(4.24), 'movieId': 246}







# -------------------------------------------------------
# Page Body 
with st.container():
    st.subheader("Collaborative Filtering")

    with st.container(key='user-selection-container'):
        st.write("* Collaborative filtering only works on Historical user data it won't work new user.")
        st.write("* We select random user and their data to understanding colloborative filtering.")
        st.write("Please select user.")
        with st.container(key='user-selection-search-container'):
            user_ids = [int(item['user_id']) for item in users_data]
            user_ids.sort()
            selected_userId = st.selectbox(label="Select User id",options=user_ids,width=400)

            if st.button("Continue"):
                st.session_state['userId']= selected_userId
                

    if st.session_state['userId']:
    # fetch show selected user details
        select_user_details =  [item for item in users_data if item['user_id'] == str(selected_userId)]
        
        show_user_profile(select_user_details[0])

    st.space()
    if st.session_state['userId']:
        # call collaborative filtering to get top recommended movies.
        recommanded_movies_list =  collaborative_based_filtering(st.session_state['userId'])
        st.subheader('Recommended Movies')

        # display the collaborative filtering movies inside the container.
        with st.container(key = 'collaborative-recom-movies-con'):
            

            with st.container(key = 'rm-collaborative-lay1-container'):
                # 1-5 movie
                rm_layer1_col =st.columns(5)
                for i in range(0,5):
                    with rm_layer1_col[i]:                                
                        movie_card(recommanded_movies_list[i])

            with st.container(key = 'rm-collaborative-lay2-container'):
                # 6-10 movie
                rm_layer2_col =st.columns(5)
                for i in range(0,5):
                    with rm_layer2_col[i]:
                        movie_card(recommanded_movies_list[5:][i])


                
            
            # st.json(recommanded_movies_list)




        
            
