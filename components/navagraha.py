import streamlit as st
import os

# ==========================================================
# Navagraha Data
# ==========================================================

NAVAGRAHA = [

    {
        "name": "Surya",
        "modern": "Sun",
        "day": "Sunday",
        "description": "Surya is regarded as the source of light and energy. In modern astronomy, Surya is the Sun, the central star of our Solar System.",
        "importance": "Provides light, heat and supports life on Earth.",
        "image": "assets/navagraha/surya.jpg"
    },

    {
        "name": "Chandra",
        "modern": "Moon",
        "day": "Monday",
        "description": "Chandra represents the Moon and is associated with lunar cycles and timekeeping.",
        "importance": "Controls tides and influences lunar calendars.",
        "image": "assets/navagraha/chandra.jpg"
    },

    {
        "name": "Mangala",
        "modern": "Mars",
        "day": "Tuesday",
        "description": "Mangala corresponds to the planet Mars.",
        "importance": "Known as the Red Planet in modern astronomy.",
        "image": "assets/navagraha/mangala.jpg"
    },

    {
        "name": "Budha",
        "modern": "Mercury",
        "day": "Wednesday",
        "description": "Budha represents Mercury, the closest planet to the Sun.",
        "importance": "Fastest orbiting planet.",
        "image": "assets/navagraha/budha.jpg"
    },

    {
        "name": "Brihaspati",
        "modern": "Jupiter",
        "day": "Thursday",
        "description": "Brihaspati represents Jupiter, the largest planet in the Solar System.",
        "importance": "Largest planet with many moons.",
        "image": "assets/navagraha/brihaspati.jpg"
    },

    {
        "name": "Shukra",
        "modern": "Venus",
        "day": "Friday",
        "description": "Shukra represents Venus, the brightest planet visible from Earth.",
        "importance": "Known as the Morning and Evening Star.",
        "image": "assets/navagraha/shukra.jpg"
    },

    {
        "name": "Shani",
        "modern": "Saturn",
        "day": "Saturday",
        "description": "Shani represents Saturn, famous for its rings.",
        "importance": "Second-largest planet in the Solar System.",
        "image": "assets/navagraha/shani.jpg"
    },

    {
        "name": "Rahu",
        "modern": "Ascending Lunar Node",
        "day": "-",
        "description": "Rahu is not a physical planet but the ascending node of the Moon's orbit.",
        "importance": "Associated with eclipse calculations.",
        "image": "assets/navagraha/rahu.jpg"
    },

    {
        "name": "Ketu",
        "modern": "Descending Lunar Node",
        "day": "-",
        "description": "Ketu represents the descending node of the Moon's orbit.",
        "importance": "Also associated with eclipse calculations.",
        "image": "assets/navagraha/ketu.jpg"
    }

]


# ==========================================================
# Display Function
# ==========================================================

def show_navagraha():

    st.header("Navagraha")

    st.write(
        "The Navagraha are the nine celestial bodies recognized in the Indian Knowledge System."
    )

    st.divider()

    for graha in NAVAGRAHA:

        with st.container(border=True):

            col1, col2 = st.columns([1,3])

            with col1:

                if os.path.exists(graha["image"]):
                    st.image(graha["image"], use_container_width=True)
                else:
                    st.info("Image Coming Soon")

            with col2:

                st.subheader(graha["name"])

                st.write(f"**Modern Equivalent:** {graha['modern']}")

                st.write(f"**Associated Day:** {graha['day']}")

                st.write(graha["description"])

                st.info(
                    f"Scientific Importance: {graha['importance']}"
                )

                st.button(
                    "Explain with AI",
                    key=graha["name"]
                )

        st.divider()