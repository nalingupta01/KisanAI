"""
KisanAI - Disease Detector (OPTIONAL / STRETCH MODULE)
----------------------------------------------------------
Build this LAST, after the other 4 modules work. It calls the free
tier of the Plant.id API to identify plant diseases from a photo -
no need to train your own image-classification model.

IMPORTANT: Third-party API request/response formats change over time.
Before wiring this in, check the current docs at https://web.plant.id/
and adjust the endpoint/payload below if needed. This is written to
match Plant.id's health-assessment endpoint as documented recently,
but always verify against their live docs first.
"""

import base64
import requests

HEALTH_ASSESSMENT_URL = "https://api.plant.id/v3/health_assessment"

# Minimal, farmer-friendly treatment tips for common diseases.
# Extend this as you test with real photos and see what disease names
# the API returns.
TREATMENT_TIPS = {
    "default": {
        "en": "Disease detected. Consult your local Krishi Vigyan Kendra "
              "for confirmation and recommended pesticide dosage.",
        "hi": "Rog paaya gaya hai. Sahi dawa aur matra ke liye apne nazdiki "
              "Krishi Vigyan Kendra se sampark karein.",
    },
}


def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


def diagnose_leaf(image_bytes, api_key):
    """
    Sends a leaf photo to Plant.id and returns a simplified result dict:
    {"disease": str, "confidence": float} or {"error": str}.
    """
    payload = {
        "images": [encode_image(image_bytes)],
        "similar_images": True,
    }
    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(HEALTH_ASSESSMENT_URL, json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        suggestions = (
            data.get("result", {})
                .get("disease", {})
                .get("suggestions", [])
        )
        if not suggestions:
            return {"disease": "No disease detected", "confidence": 0.0}

        top = suggestions[0]
        return {
            "disease": top.get("name", "Unknown"),
            "confidence": round(top.get("probability", 0) * 100, 1),
        }
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_treatment_tip(disease_name, lang="en"):
    tip = TREATMENT_TIPS.get(disease_name, TREATMENT_TIPS["default"])
    return tip.get(lang, tip["en"])