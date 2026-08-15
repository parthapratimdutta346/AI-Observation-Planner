import streamlit as st
import os
from components.ai_utils import ask_ai
# ==========================================================
# Scholar Data
# ==========================================================

SCHOLARS = [

    {
        "name": "Aryabhata",
        "period": "476 – 550 CE",
        "book": "Aryabhatiya",
        "image": "assets/aryabhata.jpg",
        "about": "Aryabhata was one of India's greatest mathematicians and astronomers. He proposed that the Earth rotates on its axis and developed methods to calculate eclipses and planetary motion.",
        "contributions": [
            "Explained Earth's rotation",
            "Calculated Solar & Lunar eclipses",
            "Approximation of π (Pi)",
            "Introduced Trigonometry",
            "Developed astronomical calculations"
        ],
        "fun_fact": "Aryabhata calculated the length of a year with remarkable accuracy."
    },

    {
        "name": "Varahamihira",
        "period": "505 – 587 CE",
        "book": "Panchasiddhantika",
        "image": "assets/varahamihira.jpg",
        "about": "Varahamihira compiled ancient astronomical knowledge and improved planetary calculations.",
        "contributions": [
            "Planetary Motion",
            "Weather Prediction",
            "Astronomical Observations",
            "Calendar Calculations"
        ],
        "fun_fact": "He combined knowledge from several ancient astronomical schools."
    },

    {
        "name": "Brahmagupta",
        "period": "598 – 668 CE",
        "book": "Brahmasphutasiddhanta",
        "image": "assets/brahmagupta.jpg",
        "about": "Brahmagupta introduced rules for zero and improved planetary mathematics.",
        "contributions": [
            "Rules of Zero",
            "Negative Numbers",
            "Planetary Calculations",
            "Astronomical Equations"
        ],
        "fun_fact": "His work influenced astronomy in India and the Middle East."
    },

    {
        "name": "Bhaskara II",
        "period": "1114 – 1185 CE",
        "book": "Siddhanta Shiromani",
        "image": "assets/bhaskara_ii.jpg",
        "about": "Bhaskara II expanded mathematical astronomy and improved eclipse prediction.",
        "contributions": [
            "Calculus Concepts",
            "Planetary Motion",
            "Astronomy",
            "Eclipse Calculations"
        ],
        "fun_fact": "Many of his ideas anticipated concepts used in calculus."
    },

    {
        "name": "Lagadha",
        "period": "1200 BCE",
        "book": "Vedanga Jyotisha",
        "image": "assets/lagadha.jpg",
        "about": "Lagadha authored Vedanga Jyotisha, one of the oldest Indian astronomical texts.",
        "contributions": [
            "Ancient Calendar",
            "Time Measurement",
            "Season Calculation"
        ],
        "fun_fact": "Vedanga Jyotisha is among the earliest surviving Indian astronomy texts."
    }

]


# ==========================================================
# Display Function
# ==========================================================

def show_scholars():

    st.title("👨‍🔬 Great Indian Astronomers")

    st.markdown("""
Learn about the pioneers of Indian astronomy whose discoveries shaped our understanding
of the universe and continue to inspire modern scientific research.
""")

    st.divider()

    # Search Box
    search = st.text_input(
        "🔍 Search Scholar",
        placeholder="Aryabhata, Varahamihira..."
    )

    if search:
        scholars = [
            s for s in SCHOLARS
            if search.lower() in s["name"].lower()
        ]
    else:
        scholars = SCHOLARS

    if len(scholars) == 0:
        st.warning("No scholar found.")
        return

    # Display Cards
    for scholar in scholars:

        with st.container(border=True):

            left, right = st.columns([1, 3])

            # Image
            with left:

                if os.path.exists(scholar["image"]):
                    st.image(
                        scholar["image"],
                        use_container_width=True
                    )
                else:
                    st.info("📷 Image not available")

            # Details
            with right:

                st.subheader(f"👤 {scholar['name']}")

                st.caption(f"📅 {scholar['period']}")

                st.markdown(
                    f"**📖 Major Work:** {scholar['book']}"
                )

                st.write(scholar["about"])

                with st.expander("🌟 Major Contributions", expanded=True):

                    for item in scholar["contributions"]:
                        st.markdown(f"✅ {item}")

                st.success(
                    f"💡 **Fun Fact:** {scholar['fun_fact']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "📚 Learn More",
                        key=f"learn_{scholar['name']}"
                    ):
                        st.info(
                            "Detailed biography will be added in the next update."
                        )

                with col2:

                    if st.button(
                            "🤖 Explain with AI",
                            key=f"ai_{scholar['name']}",
                            use_container_width=True
                    ):
                        prompt = f"""
                You are an expert in Ancient Indian Astronomy and the Indian Knowledge System (IKS).

                Explain the following ancient Indian astronomer in a simple and educational manner.

                Scholar Details
                ---------------
                Name: {scholar['name']}
                Period: {scholar['period']}
                Major Work: {scholar['book']}

                About:
                {scholar['about']}

                Major Contributions:
                {chr(10).join("- " + c for c in scholar['contributions'])}

                Interesting Fact:
                {scholar['fun_fact']}

                Instructions:
                1. Start with a brief introduction.
                2. Explain the scholar's major discoveries.
                3. Explain how these discoveries influenced astronomy.
                4. Compare their work with modern astronomy where appropriate.
                5. Mention why this scholar is important in the Indian Knowledge System (IKS).
                6. End with one interesting takeaway.
                7. Use headings and bullet points.
                8. Keep the explanation beginner-friendly.
                """

                        with st.spinner("Generating AI explanation..."):
                            answer = ask_ai(prompt)

                        st.success("✨ AI Generated Explanation")

                        with st.expander("📖 View AI Explanation", expanded=True):
                            st.markdown(answer)

        st.markdown("<br>", unsafe_allow_html=True)