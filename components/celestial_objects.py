import streamlit as st
import pandas as pd
import os


# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("astronomy_master_kb.csv")


# ==========================================================
# Celestial Objects Page
# ==========================================================

def show_celestial_objects():

    st.header("Celestial Objects")

    st.write(
        "Explore celestial objects through Modern Astronomy and the Indian Knowledge System (IKS)."
    )

    df = load_data()

    st.divider()

    # -----------------------------
    # Search
    # -----------------------------

    search = st.text_input(
        "Search Celestial Object",
        placeholder="Sun, Jupiter, Orion..."
    )

    # -----------------------------
    # Filters
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:
        category = st.selectbox(
            "Category",
            ["All"] + sorted(df["Category"].dropna().unique().tolist())
        )

    with col2:
        equipment = st.selectbox(
            "Equipment",
            ["All"] + sorted(df["Equipment"].dropna().unique().tolist())
        )

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

    if equipment != "All":
        filtered = filtered[
            filtered["Equipment"] == equipment
        ]

    st.success(f"{len(filtered)} object(s) found")

    st.divider()

    # ==========================================================
    # Cards
    # ==========================================================

    for _, row in filtered.iterrows():

        with st.container(border=True):

            left, right = st.columns([1, 3])

            # -----------------------------
            # Image
            # -----------------------------

            with left:

                image = row.get("Image_URL")

                if pd.notna(image) and os.path.exists(str(image)):
                    st.image(image, use_container_width=True)
                else:
                    st.info("No Image")

            # -----------------------------
            # Information
            # -----------------------------

            with right:

                object_name = row["Object_Name"]

                st.subheader(object_name)

                st.caption(f"{row['Category']} • {row['Object_Type']}")

                if pd.notna(row["Alternative_Name"]):
                    st.write(f"**Alternative Name:** {row['Alternative_Name']}")

                if pd.notna(row["Sanskrit_Name"]):
                    st.write(f"**Sanskrit Name:** {row['Sanskrit_Name']}")

                if pd.notna(row["Visibility"]):
                    st.write(f"**Visibility:** {row['Visibility']}")

                if pd.notna(row["Equipment"]):
                    st.write(f"**Equipment:** {row['Equipment']}")

                if pd.notna(row["Observation_Difficulty"]):
                    st.write(
                        f"**Difficulty:** {row['Observation_Difficulty']}"
                    )

                if pd.notna(row["Best_Observation_Month"]):
                    st.write(
                        f"**Best Observation:** {row['Best_Observation_Month']}"
                    )

                st.divider()

                # -----------------------------
                # Scientific Details
                # -----------------------------

                with st.expander("Scientific Details"):

                    if pd.notna(row["Distance_AU"]):
                        st.write(f"**Distance (AU):** {row['Distance_AU']}")

                    if pd.notna(row["Distance_ly"]):
                        st.write(f"**Distance (Light Years):** {row['Distance_ly']}")

                    if pd.notna(row["Apparent_Magnitude"]):
                        st.write(
                            f"**Apparent Magnitude:** {row['Apparent_Magnitude']}"
                        )

                    if pd.notna(row["Gravity_m_s2"]):
                        st.write(f"**Gravity:** {row['Gravity_m_s2']} m/s²")

                    if pd.notna(row["Temperature_C"]):
                        st.write(f"**Temperature:** {row['Temperature_C']} °C")

                    if pd.notna(row["Number_of_Moons"]):
                        st.write(f"**Moons:** {int(row['Number_of_Moons'])}")

                # -----------------------------
                # Description
                # -----------------------------

                if pd.notna(row["Student_Description"]):
                    with st.expander("Description"):
                        st.write(row["Student_Description"])

                # -----------------------------
                # IKS Reference
                # -----------------------------

                if pd.notna(row["IKS_Reference"]):
                    with st.expander("IKS Reference"):
                        st.write(row["IKS_Reference"])

                # -----------------------------
                # Related Nakshatra
                # -----------------------------

                if pd.notna(row["Related_Nakshatra"]):
                    with st.expander("Related Nakshatra"):
                        st.write(row["Related_Nakshatra"])

                # -----------------------------
                # Ancient Text
                # -----------------------------

                if pd.notna(row["Ancient_Text"]):
                    with st.expander("Ancient Text"):
                        st.write(row["Ancient_Text"])

                # -----------------------------
                # Fun Fact
                # -----------------------------

                if pd.notna(row["Fun_Fact"]):
                    st.success(f"💡 Fun Fact: {row['Fun_Fact']}")

                # -----------------------------
                # Teacher Notes
                # -----------------------------

                if pd.notna(row["Teacher_Notes"]):
                    with st.expander("Teacher Notes"):
                        st.write(row["Teacher_Notes"])

                # -----------------------------
                # Buttons
                # -----------------------------

                c1, c2 = st.columns(2)

                with c1:
                    st.button(
                        "Learn More",
                        key=f"learn_{object_name}"
                    )

                with c2:
                    st.button(
                        "Explain with AI",
                        key=f"ai_{object_name}"
                    )

        st.divider()