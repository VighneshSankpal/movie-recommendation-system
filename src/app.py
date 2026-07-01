
import streamlit as st
import requests
import pandas as pd
import numpy as np
from utils.streamlit_functions import get_movie,getMovie_lookup
from components.style import load_css,load_css_file
from components.utils import navitagor
import os
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

MOVIEID_LOOKUP =  getMovie_lookup()

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

with st.container(key = 'free-container'):
    
    navitagor()

with st.container(key="hero-container"):

    st.markdown("""
        # 🎬 Multi-Model Explainable Movie Recommendation System

        ### Discover personalized movie recommendations using
        **Content-Based**, **Collaborative**, and **Hybrid**
        recommendation engines with transparent AI explanations.
        """)
with st.container(key='home-body'):
    st.html("""
        <div class="stats-container">

            <div class="stat-card">
                <div class="stat-icon">🎥</div>
                <div class="stat-title">Movies</div>
                <div class="stat-value">3,000</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">👥</div>
                <div class="stat-title">Users</div>
                <div class="stat-value">16K</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-title">Ratings</div>
                <div class="stat-value">25M</div>
            </div>

            <div class="stat-card">
                <div class="stat-icon">🧠</div>
                <div class="stat-title">Models</div>
                <div class="stat-value">3</div>
            </div>

        </div>
        """)
    
            # Recommendation Engines
    st.html('''
        
        <div class="section-title">
            🚀 Explore Recommendation Engines
        </div>

        <div class="engine-container">

            <div class="engine-card">

                <div class="engine-icon">🎬</div>

                <h3>Content-Based</h3>

                <p>
                    Discover movies similar to your favourite movie
                    using semantic text embeddings.
                </p>

                <ul>
                    <li>Sentence Transformers</li>
                    <li>Semantic Similarity</li>
                    <li>Explainable AI</li>
                </ul>

                <button ><a class='nav-a' href='/Content_filtering'> Explore →</a></button>

            </div>

            <div class="engine-card">

                <div class="engine-icon">👥</div>

                <h3>Collaborative</h3>

                <p>
                    Personalized recommendations based on
                    user rating behaviour.
                </p>

                <ul>
                    <li>SVD Matrix Factorization</li>
                    <li>Predicted Ratings</li>
                    <li>User Preference Learning</li>
                </ul>

                <button><a class='nav-a' href='/Collaborative_filtering'> Explore →</a></button>

            </div>

            <div class="engine-card">

                <div class="engine-icon">🤝</div>

                <h3>Hybrid</h3>

                <p>
                    Combines content similarity with collaborative
                    filtering for better recommendations.
                </p>

                <ul>
                    <li>Weighted Ranking</li>
                    <li>Balanced Recommendations</li>
                    <li>Explainable Results</li>
                </ul>

                <button><a class='nav-a'  href='/Hybrid_filtering'> Explore →</a></button>

            </div>

        </div>
            ''')

    st.html("""
        <div class="section">

            <h2 class="section-heading">
                ✨ Why This Project?
            </h2>

            <p class="section-subtitle">
                Modern recommendation system with explainable AI and multiple recommendation strategies.
            </p>

            <div class="feature-grid">

                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <h3>Explainable AI</h3>
                    <p>Understand why every movie was recommended.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">🎬</div>
                    <h3>Content Based</h3>
                    <p>Uses semantic similarity between movies.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">👥</div>
                    <h3>Collaborative</h3>
                    <p>Personalized recommendations from user ratings.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">🤝</div>
                    <h3>Hybrid Engine</h3>
                    <p>Combines content and collaborative filtering.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Interactive Dashboard</h3>
                    <p>Modern Streamlit interface with visual insights.</p>
                </div>

                <div class="feature-card">
                    <div class="feature-icon">🎞️</div>
                    <h3>Movie Explorer</h3>
                    <p>View detailed movie information and recommendations.</p>
                </div>

            </div>

        </div>
                """)

    st.html("""
<div class="section">

    <h2 class="section-heading">
        ⚙️ How It Works
    </h2>

    <p class="section-subtitle">
        End-to-end recommendation workflow.
    </p>

    <div class="workflow">

        <div class="workflow-card">
            👤
            <h3>User Input</h3>
            <p>Select a movie or user profile.</p>
        </div>

        <div class="arrow">➜</div>

        <div class="workflow-card">
            🧠
            <h3>Recommendation Engine</h3>
            <p>Content, Collaborative or Hybrid model.</p>
        </div>

        <div class="arrow">➜</div>

        <div class="workflow-card">
            💡
            <h3>Explainability</h3>
            <p>Show why the movie was recommended.</p>
        </div>

        <div class="arrow">➜</div>

        <div class="workflow-card">
            🎬
            <h3>Recommendations</h3>
            <p>Top personalized movie suggestions.</p>
        </div>

    </div>

</div>
        """)

    st.html("""
    <div class="section">

        <h2 class="section-heading">
            🛠 Technology Stack
        </h2>

        <p class="section-subtitle">
            Technologies used to build the recommendation system.
        </p>

        <div class="tech-container">

            <span class="tech-chip">Python</span>
            <span class="tech-chip">Deep Learning</span>
            <span class="tech-chip">Natural Language Processing</span>
            <span class="tech-chip">Sentence Transformers</span>
            <span class="tech-chip">Word Embeddings</span>
            <span class="tech-chip">SVD Matrix Factorization</span>
            <span class="tech-chip">Cosine Similarity</span>
            <span class="tech-chip">Streamlit</span>
            <span class="tech-chip">Hybrid Recommendation</span>
            <span class="tech-chip">Scikit-Learn</span>
            <span class="tech-chip">Surprise</span>
            <span class="tech-chip">Pandas</span>
            <span class="tech-chip">NumPy</span>
            <span class="tech-chip">TMDB API</span>
            <span class="tech-chip">MovieLens 25M</span>

        </div>

    </div>
        """)
    

    st.html(
        """
<div class="footer">

    <div class="footer-divider"></div>

    <h3>Developed by</h3>

    <h2>Vighnesh Sankpal</h2>

    <p>
        Multi-Model Explainable Movie Recommendation System
    </p>

    <div class="footer-links">

        <a href="https://github.com/VighneshSankpal" target="_blank">
            💻 GitHub
        </a>

        <a href="https://www.linkedin.com/in/vighnesh-sankpal-849929323/" target="_blank">
            💼 LinkedIn
        </a>

    </div>

    <p class="footer-version">
        Version 1.0 • © 2026
    </p>

</div>
            """
    )
# with st.container(key='explore-movie-container'):
#     st.subheader("Explore Movies")

#     movieId_layer1 = [14869, 131634, 11194, 64720, 137113]
#     layer1_col = st.columns(5)
#     for i in range(5):
#         with layer1_col[i]:
#             movie_card(movieId_layer1[i])


#     movieId_layer2 = [68726, 411, 42684, 13937, 10439]
#     layer2_col = st.columns(5)
#     for i in range(5):
#         with layer2_col[i]:
#             movie_card(movieId_layer2[i])
