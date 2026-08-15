import streamlit as st
import pandas as pd
import pandas as pd

df = pd.read_csv("nakshatra_dataset.csv")

# Import Components
from components.overview import show_overview
from components.scholars import show_scholars
from components.ancient_texts import show_ancient_texts
from components.navagraha import show_navagraha
from components.nakshatra import show_nakshatras
from components.celestial_objects import show_celestial_objects
from components.comparison import show_comparison
from components.observation_tips import show_observation_tips
from components.ai_assistant import show_ai_assistant
# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_data():
    try:
        return pd.read_csv("astronomy_master_kb.csv")
    except FileNotFoundError:
        try:
            return pd.read_csv("data/astronomy_master_kb.csv")
        except FileNotFoundError:
            st.error("astronomy_master_kb.csv not found.")
            return pd.DataFrame()


# ==========================================================
# Main Page
# ==========================================================

def show_iks_page():

    st.title("Indian Knowledge System (IKS)")

    st.markdown(
        """
Explore the rich heritage of Indian astronomy and understand how ancient
Indian scholars contributed to modern astronomical knowledge.
"""
    )

    df = load_data()

    if df.empty:
        return

    st.divider()

    # ==========================================================
    # Sidebar Navigation
    # ==========================================================

    st.sidebar.subheader("IKS Sections")

    section = st.sidebar.radio(
        "Select a Section",
        [
            "Overview",
            "Ancient Scholars",
            "Ancient Texts",
            "Navagraha",
            "Nakshatras",
            "Celestial Objects",
            "Ancient vs Modern",
            "Observation Tips",
            "AI Assistant"
        ]
    )

    st.sidebar.divider()

    search = st.sidebar.text_input(
        "Search",
        placeholder="Search scholar, text or object..."
    )

    if search:
        st.sidebar.info(f"Search: {search}")

    st.divider()

    # ==========================================================
    # Overview
    # ==========================================================

    if section == "Overview":

        show_overview(df)

    # ==========================================================
    # Ancient Scholars
    # ==========================================================

    elif section == "Ancient Scholars":

        show_scholars()

    # ==========================================================
    # Ancient Texts
    # ==========================================================

    # ==========================================================
    # Ancient Texts
    # ==========================================================

    elif section == "Ancient Texts":
        show_ancient_texts()

    # ==========================================================
    # Navagraha
    # ==========================================================

    elif section == "Navagraha":
        show_navagraha()

    # ==========================================================
    # Nakshatras
    # ==========================================================

    elif section == "Nakshatras":
        show_nakshatras()

    # ==========================================================
    # Celestial Objects
    # ==========================================================

    elif section == "Celestial Objects":
        show_celestial_objects()

    # ==========================================================
    # Ancient vs Modern
    # ==========================================================

    elif section == "Ancient vs Modern":
        show_comparison()

    # ==========================================================
    # Observation Tips
    # ==========================================================

    elif section == "Observation Tips":
        show_observation_tips()

    # ==========================================================
    # AI Assistant
    # ==========================================================

    elif section == "AI Assistant":
        show_ai_assistant()

# ==========================================================
# Run Independently
# ==========================================================

if __name__ == "__main__":
    show_iks_page()