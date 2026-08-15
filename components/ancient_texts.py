import streamlit as st
import os

# ==========================================================
# Ancient Text Data
# ==========================================================

TEXTS = [

    {
        "title": "Vedanga Jyotisha",
        "author": "Lagadha",
        "period": "1200 BCE",
        "image": "assets/texts/vedanga_jyotisha.jpg",
        "description": "Vedanga Jyotisha is one of the oldest surviving Indian texts on astronomy. It explains methods for measuring time, seasons, lunar cycles and calendars used in Vedic rituals.",
        "topics": [
            "Time Measurement",
            "Lunar Calendar",
            "Solar Calendar",
            "Seasons",
            "Astronomy"
        ],
        "importance": "It laid the foundation for Indian astronomical calculations and calendar systems."
    },

    {
        "title": "Aryabhatiya",
        "author": "Aryabhata",
        "period": "499 CE",
        "image": "assets/texts/aryabhatiya.jpg",
        "description": "Aryabhatiya is one of India's greatest mathematical and astronomical works. It discusses planetary motion, eclipses, trigonometry and mathematical calculations.",
        "topics": [
            "Earth's Rotation",
            "Planetary Motion",
            "Solar Eclipse",
            "Lunar Eclipse",
            "Trigonometry"
        ],
        "importance": "Introduced revolutionary mathematical and astronomical concepts that influenced scientists worldwide."
    },

    {
        "title": "Surya Siddhanta",
        "author": "Unknown",
        "period": "4th–5th Century CE",
        "image": "assets/texts/surya_siddhanta.jpg",
        "description": "Surya Siddhanta is an important Sanskrit treatise describing planetary motion, eclipses, time calculation and astronomical constants.",
        "topics": [
            "Planetary Motion",
            "Solar System",
            "Time Calculation",
            "Eclipses",
            "Astronomical Constants"
        ],
        "importance": "Many astronomical calculations described in this text remained in use for centuries."
    },

    {
        "title": "Panchasiddhantika",
        "author": "Varahamihira",
        "period": "6th Century CE",
        "image": "assets/texts/panchasiddhantika.jpg",
        "description": "This book combines five important astronomical traditions and presents methods for planetary calculations and calendar preparation.",
        "topics": [
            "Astronomy",
            "Planetary Motion",
            "Calendar System",
            "Observation",
            "Mathematics"
        ],
        "importance": "Preserved and summarized the astronomical knowledge of several ancient Indian schools."
    },

    {
        "title": "Siddhanta Shiromani",
        "author": "Bhaskara II",
        "period": "1150 CE",
        "image": "assets/texts/siddhanta_shiromani.jpg",
        "description": "A masterpiece of mathematics and astronomy covering algebra, geometry, planetary motion and eclipse calculations.",
        "topics": [
            "Mathematics",
            "Astronomy",
            "Gravity",
            "Planetary Motion",
            "Eclipses"
        ],
        "importance": "One of the most influential scientific works in medieval India."
    }

]


# ==========================================================
# Display Function
# ==========================================================

def show_ancient_texts():

    st.header("Ancient Astronomical Texts")

    st.write(
        "Discover the classical Sanskrit texts that shaped the development of Indian astronomy."
    )

    st.divider()

    search = st.text_input(
        "Search Text",
        placeholder="Aryabhatiya..."
    )

    if search:
        texts = [
            t for t in TEXTS
            if search.lower() in t["title"].lower()
        ]
    else:
        texts = TEXTS

    if len(texts) == 0:
        st.warning("No matching text found.")
        return

    for text in texts:

        with st.container(border=True):

            left, right = st.columns([1,3])

            # -----------------------------------------
            # Image
            # -----------------------------------------

            with left:

                if os.path.exists(text["image"]):
                    st.image(
                        text["image"],
                        use_container_width=True
                    )
                else:
                    st.info("Image Coming Soon")

            # -----------------------------------------
            # Information
            # -----------------------------------------

            with right:

                st.subheader(text["title"])

                st.caption(
                    f"Author: {text['author']} | Period: {text['period']}"
                )

                st.write(text["description"])

                with st.expander(
                    "Major Topics",
                    expanded=True
                ):

                    for topic in text["topics"]:
                        st.markdown(f"- {topic}")

                st.info(
                    f"Modern Importance: {text['importance']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Learn More",
                        key=f"learn_{text['title']}"
                    ):
                        st.info(
                            "Detailed information will be added in the next version."
                        )

                with col2:

                    if st.button(
                        "Explain with AI",
                        key=f"ai_{text['title']}"
                    ):
                        st.warning(
                            "AI integration will be available in a future update."
                        )

        st.divider()