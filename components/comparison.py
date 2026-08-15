import streamlit as st
import pandas as pd


def show_comparison():

    st.header("Ancient vs Modern Astronomy")

    st.write(
        "Compare important concepts from the Indian Knowledge System (IKS) with their modern astronomical interpretations."
    )

    st.divider()

    comparison_data = [
        {
            "IKS": "Surya",
            "Modern Astronomy": "Sun",
            "Explanation": "The central star of the Solar System that provides light and energy."
        },
        {
            "IKS": "Chandra",
            "Modern Astronomy": "Moon",
            "Explanation": "Earth's natural satellite responsible for lunar phases and tides."
        },
        {
            "IKS": "Mangala",
            "Modern Astronomy": "Mars",
            "Explanation": "The fourth planet from the Sun, known as the Red Planet."
        },
        {
            "IKS": "Budha",
            "Modern Astronomy": "Mercury",
            "Explanation": "The closest planet to the Sun."
        },
        {
            "IKS": "Brihaspati",
            "Modern Astronomy": "Jupiter",
            "Explanation": "The largest planet in the Solar System."
        },
        {
            "IKS": "Shukra",
            "Modern Astronomy": "Venus",
            "Explanation": "The brightest planet visible from Earth."
        },
        {
            "IKS": "Shani",
            "Modern Astronomy": "Saturn",
            "Explanation": "A gas giant famous for its ring system."
        },
        {
            "IKS": "Rahu",
            "Modern Astronomy": "Ascending Lunar Node",
            "Explanation": "The point where the Moon crosses the ecliptic from south to north, important in eclipse calculations."
        },
        {
            "IKS": "Ketu",
            "Modern Astronomy": "Descending Lunar Node",
            "Explanation": "The point where the Moon crosses the ecliptic from north to south, also used in eclipse calculations."
        }
    ]

    df = pd.DataFrame(comparison_data)

    st.subheader("Concept Comparison")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Ancient and Modern Views")

    topics = [
        (
            "Eclipses",
            "IKS explains eclipses using Rahu and Ketu as important celestial points in traditional astronomy and mythology.",
            "Modern astronomy explains eclipses through the alignment of the Sun, Earth and Moon."
        ),
        (
            "Calendar",
            "Traditional Panchanga combines solar and lunar calculations.",
            "Modern calendars are based on internationally accepted astronomical standards."
        ),
        (
            "Planetary Motion",
            "Ancient scholars developed mathematical models for planetary positions.",
            "Modern astronomy uses Newtonian mechanics and gravitational physics."
        ),
        (
            "Observation",
            "Observations were made using the naked eye and systematic records.",
            "Modern observations use telescopes, satellites and space missions."
        )
    ]

    for title, iks, modern in topics:

        with st.container(border=True):

            st.subheader(title)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Indian Knowledge System")
                st.write(iks)

            with col2:
                st.markdown("### Modern Astronomy")
                st.write(modern)

    st.divider()

    st.subheader("Timeline")

    timeline = pd.DataFrame(
        {
            "Period": [
                "1200 BCE",
                "499 CE",
                "6th Century",
                "1150 CE",
                "Present"
            ],
            "Milestone": [
                "Vedanga Jyotisha",
                "Aryabhata",
                "Varahamihira",
                "Bhaskara II",
                "Modern Astronomy"
            ]
        }
    )

    st.table(timeline)

    st.divider()

    st.success("Key Takeaways")

    st.markdown("""
- Ancient Indian astronomers developed sophisticated methods for observing the sky.
- Many traditional concepts have clear counterparts in modern astronomy.
- Modern astronomy explains celestial phenomena using mathematics and physics.
- Both traditions emphasize careful observation of the night sky.
""")