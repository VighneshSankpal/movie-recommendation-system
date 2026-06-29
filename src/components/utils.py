import streamlit as st

import streamlit as st
from components.style import load_css, load_css_file


def setup_page():
    st.set_page_config(
        page_title="Movie Recommendation System",
        page_icon="🎬",
        layout="wide",
    )

    st.markdown("""
    <style>
    .main .block-container {
        max-width: 100%;
        padding: 0rem;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 0rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    load_css_file("src/components/style.css")
    load_css()

    navitagor()

def navitagor():
    st.markdown("## Navigate Dashboard")
    with st.container(key='nav-container'):

        col ,col1, col2, col3, col4= st.columns(5)
        with col:
            if st.button('\n\nHome', key='home_btn',use_container_width=True):
                st.switch_page('app.py')
        with col1:
            if st.button(
                "📦\n\nContent Filtering",
                key="content_btn",
                use_container_width=True,
            ):
                st.switch_page("pages/2_Content_filtering.py")

        with col2:
            if st.button(
                "🤝\n\nCollaborative Filtering",
                key="collab_btn",
                use_container_width=True,
            ):
                st.switch_page("pages/3_Collaborative_filtering.py")

        with col3:
            if st.button(
                "🎬\n\nMovie Info",
                key="movie_btn",
                use_container_width=True,
            ):
                st.switch_page("pages/4_Movie_info.py")

        with col4:
            if st.button(
                "🎬\n\Hybrid Filtering",
                key="hybrid_btn",
                use_container_width=True,
            ):
                st.switch_page("pages/5_Hybrid_filtering.py")