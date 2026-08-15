import os
import requests
import streamlit as st

from geopy.geocoders import Nominatim
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise Exception("OPENWEATHER_API_KEY is not configured.")


# ---------------------------------------------------------
# Geocoder
# ---------------------------------------------------------

geolocator = Nominatim(
    user_agent="ai_observation_planner"
)


@st.cache_data(ttl=3600)
def get_coordinates(location):
    """
    Convert a location name to latitude and longitude.
    """

    place = geolocator.geocode(location)

    if place is None:
        raise Exception(f"Location not found: {location}")

    return place.latitude, place.longitude


# ---------------------------------------------------------
# Current Weather
# ---------------------------------------------------------

@st.cache_data(ttl=300)
def get_weather(lat, lon):
    """
    Get current weather from OpenWeatherMap.
    """

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "main" not in data:
        raise Exception(f"Weather API Error: {data}")

    # OpenWeather timezone offset in seconds
    timezone_offset = data.get("timezone", 0)

    location_timezone = timezone(
        timedelta(seconds=timezone_offset)
    )

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],

        "cloud_cover": data["clouds"]["all"],

        # OpenWeather gives wind speed in m/s
        "wind_speed": data["wind"]["speed"],

        # Convert meters to kilometers
        "visibility": data.get("visibility", 10000) / 1000,

        "weather_description": data["weather"][0]["description"],

        "sunrise": datetime.fromtimestamp(
            data["sys"]["sunrise"],
            tz=timezone.utc
        ).astimezone(location_timezone),

        "sunset": datetime.fromtimestamp(
            data["sys"]["sunset"],
            tz=timezone.utc
        ).astimezone(location_timezone),

        "timezone_offset": timezone_offset,
    }


# ---------------------------------------------------------
# Forecast Weather
# ---------------------------------------------------------

@st.cache_data(ttl=300)
def get_forecast_weather(lat, lon, target_datetime):
    """
    Get the OpenWeather forecast nearest to the
    selected observation date and time.

    OpenWeather /forecast provides forecast values
    at approximately 3-hour intervals.
    """

    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if "list" not in data:
        raise Exception(f"Forecast API Error: {data}")

    # -----------------------------------------------------
    # Get location timezone from OpenWeather
    # -----------------------------------------------------

    timezone_offset = data["city"].get("timezone", 0)

    location_timezone = timezone(
        timedelta(seconds=timezone_offset)
    )

    # -----------------------------------------------------
    # Make target_datetime timezone-aware
    # -----------------------------------------------------

    if target_datetime.tzinfo is None:

        # The Streamlit-selected time is assumed
        # to be local time at the observation location.
        target_datetime = target_datetime.replace(
            tzinfo=location_timezone
        )

    else:
        target_datetime = target_datetime.astimezone(
            location_timezone
        )

    # -----------------------------------------------------
    # Find nearest forecast
    # -----------------------------------------------------

    nearest = None
    smallest_difference = None

    for item in data["list"]:

        # OpenWeather dt is Unix timestamp in UTC
        forecast_utc = datetime.fromtimestamp(
            item["dt"],
            tz=timezone.utc
        )

        # Convert forecast to local observation timezone
        forecast_local = forecast_utc.astimezone(
            location_timezone
        )

        difference = abs(
            forecast_local - target_datetime
        )

        if (
            smallest_difference is None
            or difference < smallest_difference
        ):
            smallest_difference = difference
            nearest = item

    if nearest is None:
        raise Exception(
            "No forecast available for the selected date/time."
        )

    # -----------------------------------------------------
    # Convert selected forecast timestamp
    # -----------------------------------------------------

    forecast_utc = datetime.fromtimestamp(
        nearest["dt"],
        tz=timezone.utc
    )

    forecast_local = forecast_utc.astimezone(
        location_timezone
    )

    # -----------------------------------------------------
    # Sunrise / Sunset
    # -----------------------------------------------------

    sunrise = datetime.fromtimestamp(
        data["city"]["sunrise"],
        tz=timezone.utc
    ).astimezone(location_timezone)

    sunset = datetime.fromtimestamp(
        data["city"]["sunset"],
        tz=timezone.utc
    ).astimezone(location_timezone)

    # -----------------------------------------------------
    # Return weather data
    # -----------------------------------------------------

    return {

        # Temperature in Celsius
        "temperature": nearest["main"]["temp"],

        # Relative humidity %
        "humidity": nearest["main"]["humidity"],

        # Atmospheric pressure hPa
        "pressure": nearest["main"]["pressure"],

        # Cloud cover %
        "cloud_cover": nearest["clouds"]["all"],

        # Wind speed in m/s
        "wind_speed": nearest["wind"]["speed"],

        # Visibility converted from meters to km
        "visibility": nearest.get(
            "visibility",
            10000
        ) / 1000,

        # Weather condition
        "weather_description": nearest["weather"][0][
            "description"
        ],

        # Probability of precipitation %
        "precipitation_probability": nearest.get(
            "pop",
            0
        ) * 100,

        # Local forecast time actually used
        "forecast_time": forecast_local.strftime(
            "%Y-%m-%d %H:%M"
        ),

        # UTC forecast time
        "forecast_time_utc": forecast_utc.strftime(
            "%Y-%m-%d %H:%M UTC"
        ),

        # How far the selected time was from the
        # available OpenWeather forecast
        "forecast_difference_minutes": round(
            smallest_difference.total_seconds() / 60,
            1
        ),

        "sunrise": sunrise,

        "sunset": sunset,

        "timezone_offset": timezone_offset,
    }