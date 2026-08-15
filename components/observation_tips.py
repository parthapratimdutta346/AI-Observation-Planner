import streamlit as st
import random
def show_observation_tips():

    st.header("Observation Tips")

    st.write(
        "Helpful recommendations for a better astronomical observation experience."
    )

    st.divider()

    tips = [
        "Allow your eyes 20 minutes to adapt to darkness.",
        "Avoid bright phone screens while observing.",
        "Use a red flashlight to preserve night vision.",
        "Check cloud cover before setting up your telescope.",
        "Begin with binoculars before using a telescope.",
        "Choose locations away from city lights for darker skies.",
        "Keep telescope lenses dry to prevent fogging.",
        "Plan observations when the Moon is less bright for deep-sky objects."
    ]

    st.info(random.choice(tips))