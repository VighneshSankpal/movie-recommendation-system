import streamlit as st
from components.utils import setup_page
import pandas as pd
import numpy as np
import json
from utils.streamlit_functions import getMovie_lookup, get_movie
from utils.recommendation_method import get_movies_hybrid_based
setup_page()


# -------------------------------------------------------
# session state:
if 'hybrid_userId' not in st.session_state:
    st.session_state['hybrid_userId'] = None

if 'hybrid_movieId' not in st.session_state:
    st.session_state['hybrid_movieId'] = None


if 'hybrid_movie_btn_click' not in st.session_state:
    st.session_state['hybrid_movie_btn_click'] = None




# -------------------------------------------------------
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

def get_hybrid_score(movie):
    normalized_rating = (movie.predicted_rating -0.5)/(5-0.5)
    similarity_score = movie.similarity_score
    return round((similarity_score*normalized_rating)*100,2)


def show_movie_card(movie):

    with st.container(border=True):

        poster_path  = movie_posterPath.loc[movie_posterPath['tmdb_movieId']==movie.movie_id,'poster_path'].values[0]
        if poster_path == 'unknown':

                data = get_movie(movie.movie_id)

                if data is None:
                    return

                poster_path = data.get("poster_path")
                

                movie_posterPath.loc[movie_posterPath['tmdb_movieId']==movie.movie_id,'poster_path'] = poster_path
                movie_posterPath.to_csv('dataset/processed/movieId_poster.csv',index=False)
            

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"

            st.image(poster_url, width=300)
        movie_title = str(movie.movie_title)
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


        # Final score
        st.metric(
            "⭐ Hybrid Match",
            f"{get_hybrid_score(movie)}%"
        )

        with st.expander("More Details"):

            
      

            st.metric(
                "Predicted Rating",
                f"{movie.predicted_rating:.2f}/5"
            )

            st.divider()


            if movie.matching_gernes:
                st.markdown("**Shared Genres**")
                st.write(f'''<i>{", ".join(movie.matching_gernes)}</i>''',unsafe_allow_html=True)

            if movie.matching_keywords:
                st.markdown("**Common Themes**")
                st.write(f'''<i>{", ".join(movie.matching_keywords)} </i>''',unsafe_allow_html=True)

            st.markdown("**Story Similarity**")
            similarity_plot = movie.overview_similarity
            st.progress(round(similarity_plot))

            st.write(
                f"{movie.overview_similarity:.1f}%"
            )

            st.markdown("**Director**")

            if movie.matching_director:
                st.success("Same Director")
            else:
                st.caption("Different Director")
    
# -------------------------------------------------------
# Variable Initialization
users_data = get_users_data()
MOVIEID_LOOKUP = getMovie_lookup()



# movie poster url mapping file
movie_posterPath = pd.read_csv('dataset/processed/movieId_poster.csv')




# -------------------------------------------------------
# Page Body 
with st.container(key = 'hybrid-page-body'):
    with st.container():
        st.html("""
        <div class="hybrid-banner">

    <div class="hybrid-header">

        <div class="hybrid-icon">🤝</div>

        <div>

            <h2>Hybrid Recommendation Engine</h2>

            <p>
                Combines Content-Based Filtering and Collaborative Filtering
                to generate more personalized and accurate movie recommendations.
            </p>

        </div>

    </div>

    <div class="workflow">

        <div class="workflow-box">


            <h4>Selected Movie</h4>

            <p>Captures movie characteristics using semantic embeddings.</p>

        </div>

        <div class="workflow-arrow">➜</div>

        <div class="workflow-box">



            <h4>User Profile</h4>

            <p>Learns user preferences from historical movie ratings.</p>

        </div>

        <div class="workflow-arrow">➜</div>

        <div class="workflow-box">

     

            <h4>Hybrid Ranking</h4>

            <p>Combines both recommendation scores into one final ranking.</p>

        </div>

        <div class="workflow-arrow">➜</div>

        <div class="workflow-box">

    
            <h4>Recommendations</h4>

            <p>Displays explainable movie recommendations tailored to the user.</p>

        </div>

    </div>

</div>
            """)
    

    with st.container(key='user-movie-selection-section'):
        st.markdown("### 🎬 Content-Based Recommendation")
        st.caption("Choose a movie and we'll recommend similar movies.")

        # user and movie id selection container
        col1,col2,col3 = st.columns([3,3,1], vertical_alignment='bottom')

        with col1:
            # User Id
            user_ids = [str(item['user_id']) for item in users_data]
            user_ids.sort()
            st.write("User Id")
            selected_userId = st.selectbox(label='Select User Id',
                                           options=user_ids,
                                           key='stSelectbox2',
                                           label_visibility='collapsed',
                                           

                                           )

        with col2:    
            # Movie Id:
            st.write("Movie Id")
            all_movies = MOVIEID_LOOKUP['title_clean'].unique().tolist()
            all_movies.sort()

            selected_movie = st.selectbox(label='Select Movie',
                                           options=all_movies[70:],
                                           placeholder='select movie',
                                           label_visibility='collapsed',
                                           key='stSelectbox'
                                           )

            
        with col3:
            recommend =  st.button('Recommend',key='recommend_btn',use_container_width=True)

            if recommend:
                st.session_state['hybrid_userId'] = selected_userId
                movie_id = MOVIEID_LOOKUP.loc[MOVIEID_LOOKUP['title_clean']== selected_movie,'tmdb_movieId'].values[0]

                st.session_state['hybrid_movieId'] = movie_id
                st.session_state['hybrid_movie_btn_click']=True

            
        if st.session_state['hybrid_movie_btn_click']:
            select_user_details =  [item for item in users_data if item['user_id'] == str(selected_userId)]        
            show_user_profile(select_user_details[0])
        

            top_rms = get_movies_hybrid_based(user_id=st.session_state['hybrid_userId'],
                                              tmdb_movie_id=st.session_state['hybrid_movieId'])
            


            try:
                movie_details = get_movie(st.session_state['hybrid_movieId'])
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

            # Movies 1-5 showing

            with st.container(key='rm-content-lay1-container'):
                st.subheader("Recommended Movies")
                
                layer1_col = st.columns(5)
                for i in range(5):
                    with layer1_col[i]:
                        show_movie_card(top_rms[i])


            # Movies 6-10 showing
            with st.container(key='rm-content-lay2-container'):
                layer2_col = st.columns(5)
                for i in range(5):
                    with layer2_col[i]:
                        show_movie_card(top_rms[5:][i])


            # st.write(top_rms)

            # for obj in top_rms[:5]:

                # st.write(obj.movie_title)
                # st.write(f'matching_gernes : {obj.matching_gernes}')
                # st.write(f'matching_keyword : {obj.matching_keywords}')
                # st.write(f'predicted rating : {round(obj.predicted_rating,2)}')
                # st.write(f'similarity_score : {round(obj.similarity_score,2)}')
                # st.write(f'{'*'*25}')
