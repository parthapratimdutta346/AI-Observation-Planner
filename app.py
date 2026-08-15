import streamlit as st
import prediction
import pandas as pd
from components.ai_utils import ask_ai
from components.observation_ai import generate_ai_summary
from components.about import show_about

@st.cache_data
def load_astronomy_database():
    return pd.read_csv("astronomy_master_kb.csv")

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="AI Observation Planner",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# Load Custom CSS
# ==========================================

def load_css():
    with open("styles/style.css", "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()


# ==========================================
# Sidebar
# ==========================================

st.sidebar.title("AI Observation Planner")

page = st.sidebar.radio(
    "Navigation",
    [
        "Observation Planner",
        "Sky Objects",
        "IKS Knowledge",
        "Image Analysis",
        "About"
    ]
)

# ==========================================================
# Observation Planner
# ==========================================================

if page == "Observation Planner":

    # ==========================================================
    # Hero Section
    # ==========================================================

    left, right = st.columns([1.7, 1], gap="large")

    with left:

        st.markdown("# 🌌 AI Observation Planner")

        st.markdown("### Bridging Modern Astronomy and the Indian Knowledge System")

        st.write(
            """
    Predict the best observation conditions using
    Artificial Intelligence, Machine Learning,
    Weather Analysis, Skyfield and the Indian Knowledge System.

    Explore the night sky with confidence.
            """
        )

        st.success(" AI Powered  •  IKS Integrated  •   Skyfield Astronomy")

    with right:

        st.image(
            "assets/hero.jpg",
             width="stretch"
        )

    st.divider()

    st.markdown(
        """
        <div class="section-title">
            Observation Parameters
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Enter the observation details below.")

    col1, col2, col3 = st.columns(3)

    with col1:
        location = st.text_input(
            "📍 Location",
            value="Bhubaneswar"
        )

    with col2:
        date = st.date_input(
            "📅 Observation Date"
        )

    with col3:
        time = st.time_input(
            "🕒 Observation Time"
        )

    st.divider()
    # ==========================================
    # Predict Observation
    # ==========================================

    if st.button(
            "Predict Observation",
            use_container_width=True,
            type="primary"
    ):
        with st.spinner("Analyzing astronomical conditions..."):
            st.session_state.pop("ai_summary", None)

            st.session_state["result"] = prediction.predict_observation(
                location=location,
                date=date,
                time=time
            )

    # ==========================================
    # Display Results
    # ==========================================

    if "result" in st.session_state:

        result = st.session_state["result"]

        st.success("Observation Analysis Completed")



        # ==========================================
        # Observation Summary
        # ==========================================

        st.subheader("Observation Summary")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Observation Score",
                f"{result['Observation_Score']}/100"
            )
            st.progress(result["Observation_Score"] / 100)

        with c2:
            st.metric(
                "Sky Quality",
                result["Quality"]
            )

        with c3:
            st.metric(
                "Darkness Score",
                f"{result['Darkness_Score']}/100"
            )
            st.progress(result["Darkness_Score"] / 100)

        with c4:
            st.metric(
                "Visibility",
                f"{result['Visibility']:.1f} km"
            )

        st.divider()



        # ==========================================
        # Observation Status
        # ==========================================

        st.subheader("Observation Status")

        score = result["Observation_Score"]

        if score >= 85:
            st.success(
                "Excellent observing conditions. Deep-sky and planetary observations are highly recommended."
            )

        elif score >= 70:
            st.info(
                "Good observing conditions. Most celestial objects should be clearly visible."
            )

        elif score >= 50:
            st.warning(
                "Average observing conditions. Bright objects are recommended."
            )

        else:
            st.error(
                "Poor observing conditions. Observation is not recommended."
            )

        st.divider()

        # ==========================================
        # Atmospheric & Environmental Conditions
        # ==========================================

        st.subheader("Atmospheric & Environmental Conditions")

        # ------------------------------------------
        # Atmospheric Conditions
        # ------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Atmospheric Seeing",
                result["Atmospheric_Seeing"]
            )

        with c2:
            st.metric(
                "Transparency",
                result["Transparency"]
            )
            st.progress(result["Transparency_Score"] / 100)

        with c3:
            st.metric(
                "Cloud Cover",
                f"{result['Cloud_Cover']} %"
            )

        with c4:
            st.metric(
                "Humidity",
                f"{result['Humidity']} %"
            )

        # ------------------------------------------
        # Environmental Conditions
        # ------------------------------------------

        c5, c6, c7, c8 = st.columns(4)

        with c5:
            st.metric(
                "Temperature",
                f"{result['Temperature']} °C"
            )

        with c6:
            st.metric(
                "Pressure",
                f"{result['Pressure']} hPa"
            )

        with c7:
            st.metric(
                "Wind Speed",
                f"{result['Wind_Speed']} m/s"
            )

        with c8:
            st.metric(
                "Light Pollution",
                result["Light_Pollution"]
            )

        st.caption(
            f"Coordinates: {result['Latitude']:.4f}, {result['Longitude']:.4f}"
        )

        st.caption(
            f"Weather data used: {result['Forecast_Time']}"
        )
        st.divider()

        # ==========================================
        # Astronomy Details
        # ==========================================

        st.subheader("Astronomy Details")

        c1, c2 = st.columns(2)

        # ------------------------------------------
        # Moon & Sun Information
        # ------------------------------------------

        with c1:

            st.info(
                f"""
        ### Moon & Sun

        **Moon Phase**
        {result['Moon_Phase']}

        **Moon Illumination**
        {result['Moon_Illum']} %

        **Natural Illumination**
        {result['Natural_Illumination']}

        **Moon Rise / Set**
        {result['Moon_RiseSet']}

        **Sun Rise / Set**
        {result['Sun_RiseSet']}

        **Day Length**
        {result['Day_Length']}
        """
            )

        # ------------------------------------------
        # Sky Objects
        # ------------------------------------------

        with c2:

            st.info(
                f"""
        ### Visible Sky

        **Visible Planets**
        {result['Visible_Planets']}

        **Visible Constellations**
        {result['Visible_Constellations']}

        **Nakshatra**
        {result['Nakshatra']}
        """
            )

        st.divider()

        # ==========================================
        # Observation Suitability
        # ==========================================

        st.subheader("Observation Suitability")

        score = result["Observation_Score"]

        if score >= 85:
            st.success(
                """
        Excellent observing conditions.

        Recommended:
        • Deep Sky Objects
        • Galaxies
        • Nebulae
        • Star Clusters
        • Planetary Observation
        """
            )

        elif score >= 70:
            st.info(
                """
        Good observing conditions.

        Recommended:
        • Planets
        • Bright Nebulae
        • Star Clusters
        • Double Stars
        """
            )

        elif score >= 50:
            st.warning(
                """
        Moderate observing conditions.

        Recommended:
        • Moon
        • Jupiter
        • Saturn
        • Bright Stars
        """
            )

        else:
            st.error(
                """
        Poor observing conditions.

        Recommended:
        • Moon Observation
        • Indoor Planning
        • Astrophotography Planning
        """
            )

        st.divider()



        # ==========================================
        # Observation Analysis
        # ==========================================

        st.subheader("Observation Analysis")

        strengths = []
        limitations = []

        # -------------------------
        # Strengths
        # -------------------------

        if result["Darkness_Score"] >= 70:
            strengths.append("Dark sky conditions are favorable for observation.")

        if result["Cloud_Cover"] <= 30:
            strengths.append("Low cloud cover provides a clearer view of the sky.")

        if result["Atmospheric_Seeing"] in ["Excellent", "Good"]:
            strengths.append("Atmospheric seeing is suitable for telescope observations.")

        if result["Transparency"] in ["Excellent", "Good"]:
            strengths.append("Atmospheric transparency is good for deep-sky viewing.")

        if result["Moon_Illum"] <= 30:
            strengths.append("Low moon illumination reduces natural sky brightness.")

        # -------------------------
        # Limitations
        # -------------------------

        if result["Cloud_Cover"] > 50:
            limitations.append("High cloud cover may obstruct celestial objects.")

        if result["Moon_Illum"] > 70:
            limitations.append("Bright moonlight may reduce the visibility of faint objects.")

        if result["Atmospheric_Seeing"] == "Poor":
            limitations.append("Poor atmospheric seeing may blur telescope images.")

        if result["Transparency"] == "Poor":
            limitations.append("Low atmospheric transparency may reduce object clarity.")

        if result["Visibility"] < 5000:
            limitations.append("Low visibility may affect observation quality.")

        col1, col2 = st.columns(2)

        with col1:

            st.success("Strengths")

            if strengths:
                for item in strengths:
                    st.write(f"• {item}")
            else:
                st.write("No significant strengths identified.")

        with col2:

            st.warning("Limitations")

            if limitations:
                for item in limitations:
                    st.write(f"• {item}")
            else:
                st.write("No significant limitations identified.")

        st.divider()

        # ==========================================
        # Observation Tips
        # ==========================================

        st.subheader("Today's Observation Tips")

        tips = []

        if result["Cloud_Cover"] > 60:
            tips.append("High cloud cover may block faint celestial objects.")

        if result["Moon_Illum"] > 70:
            tips.append("Bright moonlight may reduce the visibility of galaxies and nebulae.")

        if result["Wind_Speed"] > 6:
            tips.append("Strong winds may reduce telescope stability.")

        if result["Humidity"] > 85:
            tips.append("High humidity can cause dew formation on telescope optics.")

        if result["Atmospheric_Seeing"] == "Excellent":
            tips.append("Excellent seeing is ideal for high-magnification planetary observation.")

        if result["Darkness_Score"] >= 80:
            tips.append("Dark sky conditions are excellent for deep-sky observations.")

        if not tips:
            tips.append("Current conditions are generally suitable for astronomical observations.")

        for tip in tips:
            st.info(tip)

        st.divider()

        # ==========================================
        # AI Observation Summary
        # ==========================================

        st.subheader("AI Observation Summary")

        if "ai_summary" not in st.session_state:
            with st.spinner("AI is analyzing tonight's sky..."):
                st.session_state["ai_summary"] = generate_ai_summary(result)

        st.markdown(st.session_state["ai_summary"])

        # ==========================================
        # AI Actions
        # ==========================================

        st.subheader("🤖 AI Actions")

        st.caption(
            "Quick AI insights based on the current observation. "
            "For custom questions, use the AI Astronomy Assistant below."
        )
        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                    "Explain Observation Score",
                    key="explain_score"
            ):
                prompt = f"""
        Explain why today's observation score is
        {result['Observation_Score']}/100.

        Observation Data:

        Darkness Score: {result['Darkness_Score']}
        Cloud Cover: {result['Cloud_Cover']} %
        Humidity: {result['Humidity']} %
        Moon Illumination: {result['Moon_Illum']} %
        Atmospheric Seeing: {result['Atmospheric_Seeing']}
        Transparency: {result['Transparency']}
        """

                with st.spinner("Analyzing observation score..."):
                    explanation = ask_ai(
                        prompt,
                        use_rag=False
                    )

                st.info(explanation)

        with c2:

            if st.button(
                    "Observation Advice",
                    key="observation_advice"
            ):
                prompt = f"""
        Give practical astronomy observation advice.

        Today's Observation Data:

        {result}
        """

                with st.spinner("Generating observation advice..."):
                    advice = ask_ai(
                        prompt,
                        use_rag=False
                    )

                st.success(advice)

        st.divider()

        # ==========================================
        # Recommendations
        # ==========================================

        st.subheader("🔭 Recommended Celestial Objects")

        recommendations = result["Recommendations"]

        if recommendations.empty:

            st.warning("No suitable celestial objects found.")

        else:

            for _, row in recommendations.iterrows():

                with st.container(border=True):

                    col1, col2 = st.columns([1, 3])

                    # ------------------------------------------
                    # Image
                    # ------------------------------------------

                    with col1:

                        if pd.notna(row["Thumbnail_URL"]):
                            st.image(
                                row["Thumbnail_URL"],
                                use_container_width=True
                            )

                    # ------------------------------------------
                    # Information
                    # ------------------------------------------

                    with col2:

                        st.markdown(f"## 🌌 {row['Object_Name']}")

                        st.write(f"**Category:** {row['Category']}")

                        visibility = row["Visibility"] if pd.notna(row["Visibility"]) else "Not Available"
                        difficulty = row["Observation_Difficulty"] if pd.notna(
                            row["Observation_Difficulty"]) else "Not Available"
                        magnitude = row["Apparent_Magnitude"] if pd.notna(
                            row["Apparent_Magnitude"]) else "Not Available"
                        sanskrit = row["Sanskrit_Name"] if pd.notna(row["Sanskrit_Name"]) else "Not Available"
                        nakshatra = row["Related_Nakshatra"] if pd.notna(row["Related_Nakshatra"]) else "Not Available"

                        st.write(f"**Visibility:** {visibility}")
                        st.write(f"**Difficulty:** {difficulty}")
                        st.write(f"**Magnitude:** {magnitude}")
                        st.write(f"**Sanskrit Name:** {sanskrit}")
                        st.write(f"**Related Nakshatra:** {nakshatra}")

                        score = row["Recommendation_Score"]

                        st.progress(min(score / 100, 1.0))

                        if score >= 90:
                            rating = "⭐⭐⭐⭐⭐ Excellent"
                        elif score >= 75:
                            rating = "⭐⭐⭐⭐ Very Good"
                        elif score >= 60:
                            rating = "⭐⭐⭐ Good"
                        elif score >= 40:
                            rating = "⭐⭐ Fair"
                        else:
                            rating = "⭐ Basic"

                        st.markdown(f"### {rating}")
                        st.write(f"**Recommendation Score:** {score:.1f}/100")

                        if "Reasons" in row.index:

                            st.markdown("### ✅ Why Recommended")

                            for reason in str(row["Reasons"]).split(";"):

                                reason = reason.strip()

                                if reason:
                                    st.write(f"✔ {reason}")

                        if pd.notna(row["Student_Description"]):
                            st.info(row["Student_Description"])

                        if pd.notna(row["Fun_Fact"]):
                            st.success(f"💡 **Fun Fact**\n\n{row['Fun_Fact']}")

                        if pd.notna(row["IKS_Reference"]) or pd.notna(row["Ancient_Text"]):

                            st.markdown("### 🕉 Indian Knowledge System")

                            if pd.notna(row["IKS_Reference"]):
                                st.write(f"**Reference:** {row['IKS_Reference']}")

                            if pd.notna(row["Ancient_Text"]):
                                st.write(f"**Ancient Text:** {row['Ancient_Text']}")

                        if pd.notna(row["Reference_Link"]):
                            st.link_button(
                                "📖 Learn More",
                                row["Reference_Link"],
                                key=f"learn_{row['Object_ID']}"
                            )

        # =====================================================
        # AI Astronomy Assistant
        # =====================================================

        st.divider()

        st.subheader("🤖 AI Astronomy Assistant")

        st.write(
            "Ask questions about tonight's observation, recommended celestial objects, or astronomy."
        )

        st.markdown("#### Suggested Questions")

        st.markdown("""
        - Can I observe Saturn tonight?
        - Why is my observation score low?
        - Which celestial object should I observe first?
        - Is tonight suitable for astrophotography?
        - What equipment should I use?
        """)

        question = st.text_input(
            "Ask your astronomy question",
            placeholder="Example: Can I observe Saturn tonight?"
        )

        if st.button(
                "Ask AI",
                key="ask_ai_button",
                use_container_width=True
        ):

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                with st.spinner("Analyzing current observation..."):

                    prompt = f"""
        You are an expert Astronomy Observation Planner.

        Use ONLY the observation data below.

        Observation Score: {result['Observation_Score']}/100
        Darkness Score: {result['Darkness_Score']}/100
        Sky Quality: {result['Quality']}
        Atmospheric Seeing: {result['Atmospheric_Seeing']}
        Transparency: {result['Transparency']}
        Cloud Cover: {result['Cloud_Cover']}%
        Humidity: {result['Humidity']}%
        Temperature: {result['Temperature']}°C
        Pressure: {result['Pressure']} hPa
        Wind Speed: {result['Wind_Speed']} m/s
        Visibility: {result['Visibility']:.1f} km
        Moon Phase: {result['Moon_Phase']}
        Moon Illumination: {result['Moon_Illum']}%

        Visible Planets:
        {result['Visible_Planets']}

        Visible Constellations:
        {result['Visible_Constellations']}

        Nakshatra:
        {result['Nakshatra']}

        User Question:

        {question}

        Answer in simple English.

        If observing is not recommended,
        explain why.

        Recommend suitable celestial objects.

        Provide telescope and astrophotography advice.

        Limit your answer to about 200 words.
        """

                    try:

                        response = ask_ai(
                            prompt,
                            use_rag=False
                        )

                        st.success("AI Response")

                        st.markdown(response)

                    except Exception as e:

                        st.error(f"Unable to generate response.\n\n{e}")

# ==========================================================
# Sky Objects
# ==========================================================

elif page == "Sky Objects":

    st.title("🔭 Sky Objects")

    st.markdown(
        "Explore the Astronomy Knowledge Base with search and filters."
    )

    # ---------------------------------------
    # Load Dataset
    # ---------------------------------------

    df = load_astronomy_database()

    # ---------------------------------------
    # Statistics
    # ---------------------------------------

    st.subheader("📊 Astronomy Database")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🌌 Total Objects",
            len(df)
        )

    with c2:
        st.metric(
            "🪐 Planets",
            len(df[df["Category"] == "Solar System"])
        )

    with c3:
        st.metric(
            "⭐ Stars",
            len(df[df["Category"] == "Star"])
        )

    with c4:
        st.metric(
            "🌠 Galaxies",
            len(df[df["Category"] == "Galaxy"])
        )

    st.divider()

    # ---------------------------------------
    # Search, Filter & Sort
    # ---------------------------------------

    col1, col2 = st.columns([2, 1])

    with col1:

        search = st.text_input(
            "🔍 Search Object"
        )

    with col2:

        categories = ["All"] + sorted(df["Category"].dropna().unique())

        category = st.selectbox(
            "Category",
            categories
        )

        sort_by = st.selectbox(
            "Sort By",
            [
                "Object Name",
                "Brightest",
                "Difficulty",
                "Category"
            ]
        )

    # ---------------------------------------
    # Filtering
    # ---------------------------------------

    filtered = df.copy()

    if search:
        filtered = filtered[
            filtered["Object_Name"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if category != "All":
        filtered = filtered[
            filtered["Category"] == category
            ]

    # ---------------------------------------
    # Sorting
    # ---------------------------------------

    if sort_by == "Object Name":

        filtered = filtered.sort_values("Object_Name")

    elif sort_by == "Category":

        filtered = filtered.sort_values("Category")

    elif sort_by == "Brightest":

        # Convert magnitude to numeric when possible
        filtered["Mag"] = (
            filtered["Apparent_Magnitude"]
            .astype(str)
            .str.extract(r'(-?\d+\.?\d*)')[0]
        )

        filtered["Mag"] = pd.to_numeric(
            filtered["Mag"],
            errors="coerce"
        )

        filtered = filtered.sort_values(
            "Mag",
            ascending=True
        )

    elif sort_by == "Difficulty":

        difficulty_order = {
            "Easy": 1,
            "Moderate": 2,
            "Hard": 3
        }

        filtered["Difficulty_Order"] = (
            filtered["Observation_Difficulty"]
            .map(difficulty_order)
        )

        filtered = filtered.sort_values(
            "Difficulty_Order"
        )

    st.success(f"{len(filtered)} object(s) found.")

    st.divider()

    # ---------------------------------------
    # Object Cards
    # ---------------------------------------

    for _, row in filtered.iterrows():

        with st.container(border=True):

            left, right = st.columns([1, 3])

            # =====================================
            # Left Side - Image
            # =====================================

            with left:

                if pd.notna(row["Thumbnail_URL"]):

                    st.image(
                        row["Thumbnail_URL"],
                        use_container_width=True
                    )

                else:

                    st.info("No Image Available")

            # =====================================
            # Right Side - Information
            # =====================================

            with right:

                st.markdown(f"## 🌌 {row['Object_Name']}")

                # -----------------------------
                # Basic Information
                # -----------------------------

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.metric(
                        "Category",
                        row["Category"]
                    )

                with c2:

                    st.metric(
                        "Visibility",
                        row["Visibility"]
                    )

                with c3:

                    st.metric(
                        "Difficulty",
                        row["Observation_Difficulty"]
                    )

                c4, c5, c6 = st.columns(3)

                with c4:

                    st.metric(
                        "Magnitude",
                        row["Apparent_Magnitude"]
                    )

                with c5:

                    st.metric(
                        "Sanskrit Name",
                        row["Sanskrit_Name"]
                    )

                with c6:

                    st.metric(
                        "Best Month",
                        row["Best_Observation_Month"]
                    )

                # -----------------------------
                # Description
                # -----------------------------

                if pd.notna(row["Student_Description"]):
                    st.info(
                        row["Student_Description"]
                    )

                # -----------------------------
                # Fun Fact
                # -----------------------------

                if pd.notna(row["Fun_Fact"]):
                    st.success(
                        f"💡 **Fun Fact**\n\n{row['Fun_Fact']}"
                    )

                # -----------------------------
                # Complete Details
                # -----------------------------

                with st.expander("📖 View Complete Information"):

                    tab1, tab2, tab3 = st.tabs(
                        [
                            "🔬 Scientific",
                            "🕉 IKS",
                            "🔭 Observation"
                        ]
                    )

                    # =====================================
                    # Scientific
                    # =====================================

                    with tab1:
                        s1, s2 = st.columns(2)

                        with s1:
                            st.write(f"**Distance (AU):** {row['Distance_AU']}")
                            st.write(f"**Distance (km):** {row['Distance_km']}")
                            st.write(f"**Distance (Light Years):** {row['Distance_ly']}")
                            st.write(f"**Radius:** {row['Radius_km']} km")
                            st.write(f"**Diameter:** {row['Diameter_km']} km")

                        with s2:
                            st.write(f"**Mass:** {row['Mass_kg']}")
                            st.write(f"**Gravity:** {row['Gravity_m_s2']}")
                            st.write(f"**Temperature:** {row['Temperature_C']} °C")
                            st.write(f"**Spectral Type:** {row['Spectral_Type']}")
                            st.write(f"**Moons:** {row['Number_of_Moons']}")

                    # =====================================
                    # IKS
                    # =====================================

                    with tab2:
                        st.write(f"**Sanskrit Name:** {row['Sanskrit_Name']}")
                        st.write(f"**IKS Reference:** {row['IKS_Reference']}")
                        st.write(f"**Related Nakshatra:** {row['Related_Nakshatra']}")
                        st.write(f"**Ancient Text:** {row['Ancient_Text']}")

                    # =====================================
                    # Observation
                    # =====================================

                    with tab3:
                        st.write(f"**Visibility:** {row['Visibility']}")
                        st.write(f"**Equipment:** {row['Equipment']}")
                        st.write(f"**Observation Difficulty:** {row['Observation_Difficulty']}")
                        st.write(f"**Best Observation Month:** {row['Best_Observation_Month']}")
                        st.write(f"**Angular Size:** {row['Angular_Size']}")
                        st.write(f"**Apparent Magnitude:** {row['Apparent_Magnitude']}")

                # -----------------------------
                # Learn More
                # -----------------------------

                if pd.notna(row["Reference_Link"]):
                    st.link_button(
                        "📚 Learn More",
                        row["Reference_Link"],
                        key=f"learn_{row['Object_ID']}"
                    )

        st.divider()


# ==========================================================
# Image Analysis
# ==========================================================

elif page == "Image Analysis":

    from components.vision_ai import identify_image

    st.title("Image Analysis")

    st.markdown(
        """
Upload an astronomy-related image for AI-based object identification and knowledge retrieval.

Supported Images:
- Moon
- Planets
- Galaxies
- Nebulae
- Constellations
- Night Sky
- Telescope Images
- Ancient Astronomy Manuscripts
"""
    )

    uploaded_image = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_image:

        # Display uploaded image
        st.image(uploaded_image, use_container_width=True)

        # -----------------------------
        # Gemini Vision Analysis
        # -----------------------------
        with st.spinner("Analyzing Image..."):
            result = identify_image(uploaded_image)

        st.success("Image Analysis Completed")

        st.divider()

        # =====================================================
        # Image Analysis Report
        # =====================================================

        st.subheader("Image Analysis Report")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Primary Object",
                result["primary_object"]
            )

        with col2:
            st.metric(
                "Confidence",
                result["confidence"]
            )

        # -----------------------------
        # Description
        # -----------------------------

        st.markdown("### Description")

        st.info(result["description"])

        # -----------------------------
        # Additional Objects
        # -----------------------------

        if result["secondary_objects"]:

            st.markdown("### Additional Detected Objects")

            for obj in result["secondary_objects"]:
                st.write(f"• {obj}")

        st.divider()

        # =====================================================
        # AI Knowledge Analysis
        # =====================================================

        if result["astronomy_related"]:

            st.subheader("Astronomical Knowledge Analysis")

            # Better query for your RAG
            query = result["primary_object"]

            if result["secondary_objects"]:
                query += " " + " ".join(result["secondary_objects"])

            with st.spinner("Searching Knowledge Base..."):

                answer = ask_ai(query)

            st.markdown(answer)

        else:

            st.warning(
                "The uploaded image is not related to astronomy."
            )

# ==========================================================
# IKS Knowledge
# ==========================================================

elif page == "IKS Knowledge":

    from iks_knowledge import show_iks_page

    show_iks_page()
# ==========================================================
# About
# ==========================================================

elif page == "About":
    show_about()