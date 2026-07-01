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
        with st.expander("💡Explanation"):


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
    with st.container():

        st.html("""
                    <div class="model-banner">

                <div class="model-header">


                    <div class="model-text">

                        <h2>Collaborative Filtering</h2>

                        <p>
                            Discover personalized movie recommendations by learning from
                            historical user ratings. This model identifies hidden user
                            preferences using SVD Matrix Factorization.
                        </p>

                    </div>

                </div>

                <div class="workflow">

                    <div class="workflow-card">


                        <h4>Select User</h4>

                        <p>
                            Choose a sample user from the MovieLens dataset.
                        </p>

                    </div>

                    <div class="workflow-arrow">➜</div>

                    <div class="workflow-card">


                        <h4>Rating History</h4>

                        <p>
                            Analyze the user's previous movie ratings and preferences.
                        </p>

                    </div>

                    <div class="workflow-arrow">➜</div>

                    <div class="workflow-card">


                        <h4>SVD Model</h4>

                        <p>
                            Learn hidden relationships between users and movies using
                            matrix factorization.
                        </p>

                    </div>

                    <div class="workflow-arrow">➜</div>

                    <div class="workflow-card">


                        <h4>Recommendations</h4>

                        <p>
                            Predict ratings for unseen movies and recommend the highest
                            ranked ones.
                        </p>

                    </div>

                </div>

            </div>
                """)
        st.html("""
                <div class="info-banner">

            <div class="info-icon">
                💡
            </div>

            <div class="info-content">

                <h4>Collaborative Filtering</h4>

                <p>
                    This recommendation engine learns from a user's historical movie ratings.
                    Since new visitors have no rating history, this uses
                    <strong>sample users from the MovieLens dataset</strong>.
                    Select any user ID to explore recommendations based on that user's
                    preferences and viewing behaviour.
                </p>

            </div>

        </div>
            """)


    with st.container(key='user-selection-container',border=True):
        st.markdown("### 🎬 Collaborative-Based Recommendation")
        # st.caption("Choose a user.")


        with st.container(key='user-selection-search-container'):
            col1,col2 = st.columns([6,1],vertical_alignment='center')

            with col1:

                user_ids = [int(item['user_id']) for item in users_data]
                user_ids.sort()
                selected_userId = st.selectbox(label="Select User id",options=user_ids,label_visibility='collapsed',key='stSelectbox')

            with col2:
                recommend_btn =st.button("Recommend",disabled=selected_userId is None,use_container_width=True,key='recommend_btn')

                if recommend_btn:
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




        
            
