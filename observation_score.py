def calculate_observation_score(
    quality,
    cloud_cover,
    visibility,
    moon_illumination,
    visible_planets,
):
    """
    Calculate an observation score out of 100.
    """

    score = 0

    # -------------------------
    # Sky Quality (35 points)
    # -------------------------
    quality_scores = {
        "Excellent": 35,
        "Good": 28,
        "Fair": 18,
        "Poor": 8
    }

    score += quality_scores.get(quality, 0)

    # -------------------------
    # Cloud Cover (20 points)
    # -------------------------
    if cloud_cover <= 10:
        score += 20
    elif cloud_cover <= 30:
        score += 15
    elif cloud_cover <= 60:
        score += 10
    else:
        score += 5

    # -------------------------
    # Visibility (15 points)
    # -------------------------
    if visibility >= 10:
        score += 15
    elif visibility >= 7:
        score += 10
    elif visibility >= 5:
        score += 5

    # -------------------------
    # Moon Illumination (15 points)
    # Darker moon = better for deep sky
    # -------------------------
    if moon_illumination < 20:
        score += 15
    elif moon_illumination < 50:
        score += 10
    elif moon_illumination < 80:
        score += 5

    # -------------------------
    # Visible Planets (15 points)
    # -------------------------
    score += min(len(visible_planets) * 5, 15)

    return min(score, 100)
def observation_rating(score):

    if score >= 90:
        return "Excellent ⭐⭐⭐⭐⭐"

    elif score >= 75:
        return "Very Good ⭐⭐⭐⭐"

    elif score >= 60:
        return "Good ⭐⭐⭐"

    elif score >= 40:
        return "Fair ⭐⭐"

    else:
        return "Poor ⭐"