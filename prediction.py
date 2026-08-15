import joblib
import pandas as pd
from pathlib import Path
import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from recommendation import get_recommendations
from weather import (
    get_coordinates,
    get_weather,
    get_forecast_weather,
)
from skyfield_utils import AstronomyEngine

# ======================================================
# Load ML Model & Encoders
# ======================================================

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "quality_model.pkl")
label_encoders = joblib.load(BASE_DIR / "label_encoders.pkl")
quality_encoder = joblib.load(BASE_DIR / "quality_encoder.pkl")
feature_columns = joblib.load(BASE_DIR / "feature_columns.pkl")

# ======================================================
# Astronomy Engine
# ======================================================


astro = AstronomyEngine()
@st.cache_data
def get_cached_astronomy_report(latitude, longitude, date, time):
    return astro.get_astronomy_report(
        latitude=latitude,
        longitude=longitude,
        date=date,
        time=time
    )

# ======================================================
# Predict Sky Quality
# ======================================================

def predict_quality(user_input):

    df = pd.DataFrame([user_input])

    categorical_columns = [
        "Date",
        "Location_Name",
        "Moon_RiseSet",
        "Sun_RiseSet",
        "Visible_Planets",
        "Visible_Constellations",
        "Nakshatra",
    ]

    for col in categorical_columns:

        if col in label_encoders:

            try:
                df[col] = label_encoders[col].transform(df[col])

            except ValueError:
                # Unknown category
                df[col] = 0

    # Add missing features
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]

    prediction = model.predict(df)

    quality = quality_encoder.inverse_transform(prediction)[0]

    return quality

# ======================================================
# Astronomy Quality Metrics
# ======================================================

def calculate_seeing(wind_speed, humidity):

    if wind_speed <= 2 and humidity <= 60:
        return "Excellent"

    elif wind_speed <= 4 and humidity <= 75:
        return "Good"

    elif wind_speed <= 6 and humidity <= 90:
        return "Average"

    return "Poor"


def calculate_transparency(cloud_cover, humidity):

    score = 100 - (cloud_cover * 0.6 + humidity * 0.4)

    score = max(0, min(score, 100))

    if score >= 80:
        status = "Excellent"
    elif score >= 60:
        status = "Good"
    elif score >= 40:
        status = "Fair"
    else:
        status = "Poor"

    return round(score), status


def calculate_natural_illumination(moon_illum):

    if moon_illum <= 15:
        return "Excellent"

    elif moon_illum <= 35:
        return "Good"

    elif moon_illum <= 60:
        return "Moderate"

    elif moon_illum <= 80:
        return "Poor"

    return "Very Poor"



# ======================================================
# Darkness Score
# ======================================================

def calculate_darkness_score(moon_illum, cloud_cover, visibility):
    """
    Calculates a darkness score (0-100).

    Factors:
    - Moon Illumination (50%)
    - Cloud Cover (30%)
    - Visibility (20%)

    Higher score = Better observing conditions.

    Visibility is already provided in kilometres.
    """

    # Visibility is already in kilometres
    visibility_km = visibility

    # Visibility score (10 km or more = full score)
    visibility_score = min(visibility_km, 10) * 10

    score = (
        (100 - moon_illum) * 0.50 +
        (100 - cloud_cover) * 0.30 +
        visibility_score * 0.20
    )

    return round(max(0, min(score, 100)))

# ======================================================
# Overall Observation Score
# ======================================================

def calculate_observation_score(
    darkness_score,
    transparency_score,
    seeing
):
    """
    Calculates the overall observation score (0-100).

    Weights:
    - Darkness Score      : 45%
    - Transparency Score  : 35%
    - Atmospheric Seeing  : 20%
    """

    seeing_scores = {
        "Excellent": 100,
        "Good": 80,
        "Average": 60,
        "Poor": 40,
    }

    seeing_score = seeing_scores.get(seeing, 40)

    score = (
        darkness_score * 0.45 +
        transparency_score * 0.35 +
        seeing_score * 0.20
    )

    return round(max(0, min(score, 100)))

# ======================================================
# Observation Prediction
# ======================================================

def predict_observation(location, date, time):

    # -------------------------------------------------
    # Coordinates
    # -------------------------------------------------

    lat, lon = get_coordinates(location)

    if lat is None or lon is None:
        raise ValueError("Unable to find the specified location.")

    # ============================================
    # Weather
    # ============================================

    selected_datetime = datetime.combine(date, time)

    # Current time in India
    current_datetime = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).replace(tzinfo=None)

    time_difference = (
            selected_datetime - current_datetime
    ).total_seconds()

    days_ahead = (
            selected_datetime.date() - current_datetime.date()
    ).days

    # --------------------------------------------
    # Past observation
    # --------------------------------------------

    if time_difference < 0:

        # Selected time has already passed
        weather = get_weather(lat, lon)


    # --------------------------------------------
    # Current / future observation
    # --------------------------------------------

    elif days_ahead <= 5:

        # Use forecast nearest to selected observation time
        weather = get_forecast_weather(
            lat,
            lon,
            selected_datetime
        )


    # --------------------------------------------
    # Beyond forecast range
    # --------------------------------------------

    else:

        st.warning(
            "Weather forecast is available only "
            "for approximately the next 5 days. "
            "Using current weather conditions."
        )

        weather = get_weather(lat, lon)
        
    # -------------------------------------------------
    # Astronomy
    # -------------------------------------------------

    astronomy = get_cached_astronomy_report(
        latitude=lat,
        longitude=lon,
        date=date,
        time=time
    )

    moon_phase = astronomy["moon_phase"]
    phase_angle = astronomy["moon_phase_angle"]
    moon_illum = astronomy["moon_illumination"]

    moon_riseset = f"{astronomy['moonrise']} / {astronomy['moonset']}"
    sun_riseset = f"{astronomy['sunrise']} / {astronomy['sunset']}"

    visible_planets = (
        ", ".join(astronomy["visible_planets"])
        if astronomy["visible_planets"]
        else "Not Available"
    )

    visible_constellations = (
        ", ".join(astronomy["visible_constellations"])
        if astronomy["visible_constellations"]
        else "Not Available"
    )

    nakshatra = astronomy["nakshatra"]

    day_length = astronomy["day_length"]

    # Temporary
    light_pollution = 45

    # -------------------------------------------------
    # Astronomy Quality Metrics
    # -------------------------------------------------

    seeing = calculate_seeing(
        weather["wind_speed"],
        weather["humidity"]
    )

    transparency_score, transparency = calculate_transparency(
        weather["cloud_cover"],
        weather["humidity"]
    )

    natural_illumination = calculate_natural_illumination(
        moon_illum
    )

    darkness_score = calculate_darkness_score(
        moon_illum,
        weather["cloud_cover"],
        weather["visibility"]
    )

    observation_score = calculate_observation_score(
        darkness_score,
        transparency_score,
        seeing
    )

    # -------------------------------------------------
    # ML Input
    # -------------------------------------------------

    user_input = {

        "Date": str(date),

        "Location_Name": location,

        "Lat": lat,
        "Lon": lon,

        "Moon_Phase": phase_angle,
        "Moon_Illum": moon_illum,

        "Moon_RiseSet": moon_riseset,
        "Sun_RiseSet": sun_riseset,

        "Cloud_Cover": weather["cloud_cover"],
        "Humidity": weather["humidity"],
        "Temperature": weather["temperature"],
        "Wind_Speed": weather["wind_speed"],

        "Light_Pollution": light_pollution,

        "Visible_Planets": visible_planets,
        "Visible_Constellations": visible_constellations,

        "Nakshatra": nakshatra,
    }

    # -------------------------------------------------
    # ML Prediction
    # -------------------------------------------------

    quality = predict_quality(user_input)

    # -------------------------------------------------
    # Recommendation Engine
    # -------------------------------------------------

    recommendations = get_recommendations(
        quality=quality,
        moon_illum=moon_illum,
        cloud_cover=weather["cloud_cover"],
        visible_planets=astronomy["visible_planets"],
        visible_constellations=astronomy["visible_constellations"],
        top_n=5,
    )

    # -------------------------------------------------
    # Final Output
    # -------------------------------------------------


    return {

    # ============================================
    # Observation Quality
    # ============================================

    "Quality": quality,
    "Observation_Score": observation_score,
    "Darkness_Score": darkness_score,

    # ============================================
    # Location
    # ============================================

    "Latitude": lat,
    "Longitude": lon,

    # ============================================
    # Weather
    # ============================================

    "Temperature": weather["temperature"],
    "Humidity": weather["humidity"],
    "Pressure": weather["pressure"],
    "Cloud_Cover": weather["cloud_cover"],
    "Wind_Speed": weather["wind_speed"],
    "Visibility": weather["visibility"],


    # Actual forecast time used
    "Forecast_Time": weather.get(
        "forecast_time",
        "Current Weather"
    ),

    # ============================================
    # Astronomy
    # ============================================

    "Moon_Phase": moon_phase,
    "Moon_Phase_Angle": phase_angle,
    "Moon_Illum": moon_illum,

    "Moon_RiseSet": moon_riseset,
    "Sun_RiseSet": sun_riseset,

    "Day_Length": day_length,

    "Visible_Planets": visible_planets,
    "Visible_Constellations": visible_constellations,

    "Nakshatra": nakshatra,

    # ============================================
    # Astronomy Observation Metrics
    # ============================================

    "Atmospheric_Seeing": seeing,

    "Transparency": transparency,
    "Transparency_Score": transparency_score,

    "Natural_Illumination": natural_illumination,

    "Light_Pollution": light_pollution,

    # ============================================
    # Recommendation
    # ============================================

    "Recommendations": recommendations,
}