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
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if st.button(
            "🏠 Home",
            key="home_tab",
            use_container_width=True
        ):
            st.switch_page("app.py")

    with c2:
        if st.button(
            "🎬 Content",
            key="content_tab",
            use_container_width=True
        ):
            st.switch_page("pages/2_Content_filtering.py")

    with c3:
        if st.button(
            "👥 Collaborative",
            key="collab_tab",
            use_container_width=True
        ):
            st.switch_page("pages/3_Collaborative_filtering.py")

    with c4:
        if st.button(
            "🤝 Hybrid",
            key="hybrid_tab",
            use_container_width=True
        ):
            st.switch_page("pages/5_Hybrid_filtering.py")

    st.markdown("</div>", unsafe_allow_html=True)