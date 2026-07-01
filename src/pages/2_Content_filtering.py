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
    with st.container(border=True ):
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
        st.markdown(
            f"""
            <div style="
                height: 60px;
                font-size: 1.4rem;
                font-weight: 600;
                line-height: 1.3;
                overflow: hidden;
                margin-bottom:10px;
            ">
                {movie_title}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # if st.button(label='Check Out it', key= f'movie-show-{rm.movie_id}'):
        #     st.session_state['movie_show'] = {
        #     'movie_title' :movie_title,
        #     'movie_id' :movie_id
        # }
        #     st.switch_page(page='pages/4_Movie_info.py')
        
      

        with st.expander("💡Explanation"):

            if rm.matching_gernes:
                st.markdown("##### 🎭 Shared Genres")
                st.success(" • ".join(rm.matching_gernes))

            if rm.matching_keywords:
                st.markdown("##### 🏷️ Common Themes")
                st.info(" • ".join(rm.matching_keywords))

            st.markdown("##### 📖 Story Similarity")

            similarity = float(rm.overview_similarity)

            st.progress(int(similarity))

            st.caption(f"{similarity:.1f}% similar storyline")

            st.markdown("##### 🎬 Director")

            if rm.matching_director:
                st.success("Same director")
            else:
                st.caption("Different director")

            st.divider()

            st.markdown("##### 📝 Summary")

            summary = []

            if rm.matching_gernes:
                summary.append("shares similar genres")

            if rm.matching_keywords:
                summary.append("contains similar themes")

            if similarity >= 0.50:
                summary.append("has a closely related storyline")

            if rm.matching_director:
                summary.append("is directed by the same director")

            if summary:
                st.write(
                    "This recommendation was selected because it "
                    + ", ".join(summary[:-1])
                    + (" and " + summary[-1] if len(summary) > 1 else summary[0])
                    + "."
                )

        
        # st.write(f'Title : {movie_title if len(movie_title) <18 else movie_title[:17]+'..'}')
       




# ---------------------------------------------------------------------
# Application Layout
setup_page()

with st.container():
    with st.container():
        st.html("""
        <div class="model-banner">

    <div class="model-header">
        <div class="model-text">

            <h2>Content Based Recommendation</h2>

            <p>
                Discover movies that are similar to your favourite movie by
                analysing their genres, keywords, cast, director and plot using
                semantic embeddings.
            </p>

        </div>

    </div>

    <div class="workflow">

        <div class="workflow-card">

            
            <h4>Select Movie</h4>

            <p>
                Choose a movie you enjoyed.
            </p>

        </div>

        <div class="workflow-arrow">➜</div>

        <div class="workflow-card">


            <h4>Semantic Analysis</h4>

            <p>
                Genres, keywords, cast, director and overview are converted
                into semantic embeddings.
            </p>

        </div>

        <div class="workflow-arrow">➜</div>

        <div class="workflow-card">

            <h4>Similarity Search</h4>

            <p>
                Cosine similarity finds movies with the most similar content.
            </p>

        </div>

        <div class="workflow-arrow">➜</div>

        <div class="workflow-card">


            <h4>Recommendations</h4>

            <p>
                View the top matching movies with explainable similarity.
            </p>

        </div>

    </div>

</div>
            """)
    

    with st.container(border=True):

        st.markdown("### 🎬 Content-Based Recommendation")
        st.caption("Choose a movie and we'll recommend similar movies.")

        col1, col2 = st.columns(
            [6, 1],
            vertical_alignment="bottom"
        )

        with col1:
            selected_movie = st.selectbox(
                "Movie",
                options=all_movies[70:],
               
                placeholder="Search a movie...",
                key='stSelectbox',
                label_visibility='collapsed'
            )

        with col2:
            recommend = st.button(
                "Recommend",
                key='recommend_btn',
                 disabled=selected_movie is None,
                use_container_width=True
            )

            if recommend:
                st.session_state['movie_btn_click'] = True


    if st.session_state['movie_btn_click']:
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
            st.subheader("Recommended Movies")

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
            

        # for rmc in recommended_movies_info:
        #     st.write(f'Movie Title is : {rmc.movie_title}')
        #     st.write(f'Movie_id is : {rmc.movie_id}')
        #     st.write(f'Movie matching_keywords is : {rmc.matching_keywords}')
        #     st.write(f'Movie matching_gernes is : {rmc.matching_gernes}')
        #     st.write(f'Movie overview_similarity is : {rmc.overview_similarity}')
        #     st.write(f'Movie matching_director is : {rmc.matching_director}')
        #     st.write('-'*25)
        # st.json(movie_details)
