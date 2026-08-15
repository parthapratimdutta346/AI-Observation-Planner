import streamlit as st
import os

from components.ai_utils import ask_ai

# ==========================================================
# Nakshatra Data
# ==========================================================

NAKSHATRAS = [
    {
        "name": "Ashwini",
        "symbol": "Horse Head",
        "deity": "Ashwini Kumaras",
        "planet": "Ketu",
        "modern_star": "Beta Arietis",
        "constellation": "Aries",
        "months": "October – January",
        "visibility": "Eastern Sky",
        "equipment": "Naked Eye",
        "description": (
            "Ashwini is the first Nakshatra and marks the beginning of the "
            "zodiac. It symbolizes speed, healing and new beginnings."
        ),
        "image": "assets/nakshatra/ashwini.jpg"
    },

    {
        "name": "Bharani",
        "symbol": "Yoni",
        "deity": "Yama",
        "planet": "Venus",
        "modern_star": "35 Arietis",
        "constellation": "Aries",
        "months": "October – January",
        "visibility": "Eastern Sky",
        "equipment": "Naked Eye",
        "description": (
            "Bharani represents transformation, responsibility and the cycle of life."
        ),
        "image": "assets/nakshatra/bharani.jpg"
    },

    {
        "name": "Krittika",
        "symbol": "Razor",
        "deity": "Agni",
        "planet": "Sun",
        "modern_star": "Pleiades (M45)",
        "constellation": "Taurus",
        "months": "November – February",
        "visibility": "East",
        "equipment": "Naked Eye / Binoculars",
        "description": (
            "Krittika is associated with the famous Pleiades star cluster "
            "and symbolizes purification and courage."
        ),
        "image": "assets/nakshatra/krittika.jpg"
    },

    # Add the remaining Nakshatras here...
]

# ==========================================================
# Nakshatra Page
# ==========================================================

def show_nakshatras():

    st.header("🌟 27 Nakshatras")

    st.write(
        "Explore the 27 Nakshatras described in the Indian Knowledge System (IKS) "
        "and their relation to modern astronomy."
    )

    st.divider()

    search = st.text_input(
        "Search Nakshatra",
        placeholder="Search by name..."
    )

    if search:
        data = [
            n for n in NAKSHATRAS
            if search.lower() in n["name"].lower()
        ]
    else:
        data = NAKSHATRAS

    if not data:
        st.warning("No Nakshatra found.")
        return

    selected = st.selectbox(
        "Select Nakshatra",
        [n["name"] for n in data]
    )

    nak = next(n for n in data if n["name"] == selected)

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:

        if os.path.exists(nak["image"]):
            st.image(
                nak["image"],
                use_container_width=True
            )
        else:
            st.info("Image Coming Soon")

    with col2:

        st.subheader(nak["name"])

        st.write(f"**Symbol:** {nak['symbol']}")
        st.write(f"**Presiding Deity:** {nak['deity']}")
        st.write(f"**Ruling Planet:** {nak['planet']}")
        st.write(f"**Modern Star:** {nak['modern_star']}")
        st.write(f"**Constellation:** {nak['constellation']}")
        st.write(f"**Best Observation:** {nak['months']}")
        st.write(f"**Visibility:** {nak['visibility']}")
        st.write(f"**Recommended Equipment:** {nak['equipment']}")

        st.write("---")

        st.write(nak["description"])

    st.divider()

    # ==========================================================
    # AI Explanation
    # ==========================================================

    if st.button(
        "🤖 Explain with AI",
        key=f"ai_{nak['name']}",
        use_container_width=True
    ):

        prompt = f"""
You are an expert in Astronomy and the Indian Knowledge System (IKS).

Explain the following Nakshatra in a simple and educational manner.

Nakshatra Name:
{nak['name']}

Symbol:
{nak['symbol']}

Presiding Deity:
{nak['deity']}

Ruling Planet:
{nak['planet']}

Modern Star:
{nak['modern_star']}

Constellation:
{nak['constellation']}

Best Observation Months:
{nak['months']}

Visibility:
{nak['visibility']}

Equipment:
{nak['equipment']}

Description:
{nak['description']}

Instructions:
- Start with a short introduction.
- Explain the modern astronomy perspective.
- Explain the Indian Knowledge System (IKS) perspective.
- Explain how it can be observed.
- Mention one interesting fact.
- Use headings and bullet points.
- Keep the explanation beginner-friendly.
"""

        with st.spinner("Generating AI explanation..."):

            answer = ask_ai(prompt)

        st.success("✨ AI Generated Explanation")

        with st.expander("View Explanation", expanded=True):
            st.markdown(answer)