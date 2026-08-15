from components.ai_utils import ask_ai


def generate_ai_summary(result):

    prompt = f"""
You are an expert astronomy observation assistant.

Analyze the following observation data and generate a concise report.

Observation Data

Location:
Latitude: {result['Latitude']}
Longitude: {result['Longitude']}

Observation Score:
{result['Observation_Score']}/100

Darkness Score:
{result['Darkness_Score']}/100

Sky Quality:
{result['Quality']}

Cloud Cover:
{result['Cloud_Cover']} %

Humidity:
{result['Humidity']} %

Visibility:
{result['Visibility']/1000:.1f} km

Temperature:
{result['Temperature']} °C

Wind Speed:
{result['Wind_Speed']} m/s

Moon Phase:
{result['Moon_Phase']}

Moon Illumination:
{result['Moon_Illum']} %

Atmospheric Seeing:
{result['Atmospheric_Seeing']}

Transparency:
{result['Transparency']}

Visible Planets:
{result['Visible_Planets']}

Visible Constellations:
{result['Visible_Constellations']}

Nakshatra:
{result['Nakshatra']}

Write the response using these headings:

Overall Assessment

Why these conditions occurred

Recommended observations

Objects to avoid

Practical advice

Keep the answer below 200 words.
"""

    return ask_ai(prompt)