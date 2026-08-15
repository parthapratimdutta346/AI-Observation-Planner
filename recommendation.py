import pandas as pd
from pathlib import Path

# ==========================================
# Load Astronomy Knowledge Base
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
kb = pd.read_csv(BASE_DIR / "astronomy_master_kb.csv")


# ==========================================
# Recommendation Score Calculation
# ==========================================

def calculate_scores(
    quality,
    moon_illum,
    cloud_cover,
    visible_planets=None,
    visible_constellations=None,
):

    if visible_planets is None:
        visible_planets = []

    if visible_constellations is None:
        visible_constellations = []

    df = kb.copy()

    # ---------------------------------------
    # Remove Earth
    # ---------------------------------------

    df = df[
        df["Object_Name"]
        .fillna("")
        .str.lower() != "earth"
    ].copy()

    # ---------------------------------------
    # Initialize Score
    # ---------------------------------------

    df["Recommendation_Score"] = 0
    df["Reasons"] = ""

    # =======================================
    # Sky Quality
    # =======================================

    quality_score = {
        "Excellent": 40,
        "Good": 30,
        "Moderate": 20,
        "Poor": 10
    }

    score = quality_score.get(quality, 20)

    df["Recommendation_Score"] += score

    if quality == "Excellent":
        df["Reasons"] += "Excellent sky quality; "

    elif quality == "Good":
        df["Reasons"] += "Good observing conditions; "

    elif quality == "Moderate":
        df["Reasons"] += "Average sky quality; "

    else:
        df["Reasons"] += "Limited sky quality; "

    # =======================================
    # Cloud Cover
    # =======================================

    if cloud_cover <= 10:

        df["Recommendation_Score"] += 25
        df["Reasons"] += "Very low cloud cover; "

    elif cloud_cover <= 30:

        df["Recommendation_Score"] += 20
        df["Reasons"] += "Low cloud cover; "

    elif cloud_cover <= 60:

        df["Recommendation_Score"] += 10
        df["Reasons"] += "Moderate cloud cover; "

    else:

        df["Recommendation_Score"] += 5
        df["Reasons"] += "High cloud cover; "

    # =======================================
    # Moon Illumination
    # =======================================

    if moon_illum <= 20:
        df["Recommendation_Score"] += 20

    elif moon_illum <= 50:
        df["Recommendation_Score"] += 10

    else:
        df["Recommendation_Score"] += 5

    # =======================================
    # Naked Eye Bonus
    # =======================================

    if "Visibility" in df.columns:

        mask = (
            df["Visibility"]
            .fillna("")
            .str.lower()
            .str.contains("naked")
        )

        df.loc[mask, "Recommendation_Score"] += 10

        df.loc[
            mask,
            "Reasons"
        ] += "Can be seen with naked eye; "

    # =======================================
    # Easy Objects
    # =======================================

    if "Observation_Difficulty" in df.columns:

        easy = (
            df["Observation_Difficulty"]
            .fillna("")
            .str.lower()
            == "easy"
        )

        medium = (
            df["Observation_Difficulty"]
            .fillna("")
            .str.lower()
            == "medium"
        )

    df.loc[easy, "Recommendation_Score"] += 15
    df.loc[easy, "Reasons"] += "Easy to observe; "

    df.loc[medium, "Recommendation_Score"] += 8
    df.loc[medium, "Reasons"] += "Moderate difficulty; "

    # =======================================
    # Best Observation Month
    # =======================================

    if "Best_Observation_Month" in df.columns:

        current_month = pd.Timestamp.today().strftime("%B")

        mask = (
            df["Best_Observation_Month"]
            .fillna("")
            .str.contains(current_month, case=False)
        )

        df.loc[mask, "Recommendation_Score"] += 20

    # =======================================
    # Visible Planets
    # =======================================

    for planet in visible_planets:

        mask = (
            df["Object_Name"]
            .fillna("")
            .str.lower()
            == planet.lower()
        )

        df.loc[mask, "Recommendation_Score"] += 35

        df.loc[
            mask,
            "Reasons"
        ] += "Visible tonight; "

    # =======================================
    # Visible Constellations
    # =======================================

    if "Object_Type" in df.columns:

        for constellation in visible_constellations:

            mask = (
                df["Object_Type"]
                .fillna("")
                .str.lower()
                .str.contains(constellation.lower())
            )

            df.loc[mask, "Recommendation_Score"] += 15

    # =======================================
    # Sort
    # =======================================

    df = df.sort_values(
        by="Recommendation_Score",
        ascending=False
    )

    return df


# ==========================================
# Recommendation Function
# ==========================================

def get_recommendations(
    quality,
    moon_illum,
    cloud_cover,
    visible_planets=None,
    visible_constellations=None,
    top_n=5,
):

    recommendations = calculate_scores(
        quality=quality,
        moon_illum=moon_illum,
        cloud_cover=cloud_cover,
        visible_planets=visible_planets,
        visible_constellations=visible_constellations,
    )

    return recommendations.head(top_n)