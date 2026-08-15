import streamlit as st
import pandas as pd


def show_overview(df: pd.DataFrame):
    st.header("📖 Overview")

    st.markdown("""
### Welcome to the Indian Knowledge System (IKS)

Indian astronomy is one of the world's oldest scientific traditions. Long before
modern telescopes existed, Indian scholars carefully observed the sky and developed
methods to calculate planetary motion, eclipses, calendars, and seasons.

This module bridges **Modern Astronomy** with **Indian Knowledge Systems (IKS)**,
helping students understand celestial objects from both scientific and historical
perspectives.
""")

    st.divider()

    st.subheader("📊 Quick Statistics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🪐 Objects", len(df))

    with col2:
        st.metric("⭐ Nakshatras", 27)

    with col3:
        st.metric("☀ Navagraha", 9)

    with col4:
        st.metric("👨‍🔬 Scholars", 5)

    with col5:
        st.metric("📚 Ancient Texts", 5)

    st.divider()

    st.subheader("🎯 Learning Objectives")

    st.success("""
✔ Understand ancient Indian astronomy

✔ Learn about famous Indian astronomers

✔ Explore Nakshatras and Navagraha

✔ Compare ancient and modern astronomy

✔ Discover how celestial objects were observed in ancient India
""")

    st.divider()

    st.subheader("🕒 Timeline of Indian Astronomy")

    timeline = [
        ("1200 BCE", "Vedanga Jyotisha"),
        ("499 CE", "Aryabhata publishes Aryabhatiya"),
        ("550 CE", "Varahamihira writes Panchasiddhantika"),
        ("628 CE", "Brahmagupta develops astronomical calculations"),
        ("1150 CE", "Bhaskara II writes Siddhanta Shiromani"),
    ]

    for year, event in timeline:
        st.markdown(f"**{year}** — {event}")

    st.divider()

    st.subheader("🌌 Why Indian Astronomy Matters")

    st.info("""
Indian astronomy contributed to:

- Accurate calendars
- Eclipse prediction
- Planetary motion studies
- Timekeeping
- Navigation
- Seasonal agriculture
- Mathematical astronomy
""")

    st.divider()

    st.subheader("💡 Did You Know?")

    st.warning("""
Aryabhata proposed that the Earth rotates on its axis,
which explains the apparent movement of stars across the sky.
""")
