import os
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def identify_image(uploaded_file):

    image = Image.open(uploaded_file)

    prompt = """
You are an astronomy image analysis expert.

Analyze the uploaded image.

Return ONLY valid JSON.

{
    "astronomy_related": true,
    "primary_object": "",
    "secondary_objects": [],
    "description": "",
    "confidence": ""
}

Rules:

- If NOT astronomy related:
{
    "astronomy_related": false,
    "primary_object": "",
    "secondary_objects": [],
    "description": "Not an astronomy image.",
    "confidence": "High"
}

Do not write markdown.
Do not write explanations.
Return JSON only.
"""

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=[image, prompt]
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "astronomy_related": False,
            "primary_object": "",
            "secondary_objects": [],
            "description": response.text,
            "confidence": "Unknown"
        }