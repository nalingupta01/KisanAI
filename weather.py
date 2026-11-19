"""
KisanAI - Weather Advisory Module
------------------------------------
Fetches a 5-day / 3-hour forecast from OpenWeatherMap's free tier and
turns it into simple farming advice using plain if/else rules.
This rule engine IS your "AI logic" for the project report - it doesn't
need to be a trained ML model to be a legitimate decision-support system.
"""

import requests

FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_forecast(city, api_key):
    """
    Returns raw forecast JSON from OpenWeatherMap, or None on failure.
    Free tier gives a 5-day forecast in 3-hour steps.
    """
    params = {"q": f"{city},IN", "appid": api_key, "units": "metric"}
    try:
        resp = requests.get(FORECAST_URL, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def summarize_forecast(raw):
    """
    Collapse the 3-hour steps into one summary per day:
    max temp, min temp, total expected rain (mm), max humidity, max wind.
    """
    if not raw or "list" not in raw:
        return []

    days = {}
    for entry in raw["list"]:
        date = entry["dt_txt"].split(" ")[0]
        day = days.setdefault(date, {
            "temp_max": -100, "temp_min": 100, "rain": 0.0,
            "humidity_max": 0, "wind_max": 0.0,
        })
        day["temp_max"] = max(day["temp_max"], entry["main"]["temp_max"])
        day["temp_min"] = min(day["temp_min"], entry["main"]["temp_min"])
        day["rain"] += entry.get("rain", {}).get("3h", 0.0)
        day["humidity_max"] = max(day["humidity_max"], entry["main"]["humidity"])
        day["wind_max"] = max(day["wind_max"], entry["wind"]["speed"])

    return [{"date": d, **v} for d, v in sorted(days.items())]


def generate_advisory(daily_summary, lang="en"):
    """
    Simple, explainable rule-based advisory - this is the 'engine' you
    describe in your report as the advisory logic.
    """
    advisories = []

    for day in daily_summary:
        msgs = []

        if day["rain"] > 10:
            msgs.append({
                "en": "Rain expected - avoid sowing or spraying pesticide today.",
                "hi": "Baarish ki sambhavna hai - aaj buwai ya spray na karein.",
            })
        if day["temp_max"] > 38:
            msgs.append({
                "en": "High temperature - irrigate crops, watch for heat stress.",
                "hi": "Tapman zyada hai - sinchai karein, fasal ko paani chahiye.",
            })
        if day["temp_min"] < 8:
            msgs.append({
                "en": "Frost risk - cover sensitive crops or do light irrigation at night.",
                "hi": "Paala padne ka khatra - sanvedansheel fasal ko dhake ya raat mein halki sinchai karein.",
            })
        if day["humidity_max"] > 85:
            msgs.append({
                "en": "High humidity - fungal disease risk, monitor crops closely.",
                "hi": "Namी zyada hai - fungal rog ka khatra, fasal par nazar rakhein.",
            })
        if day["wind_max"] > 10:
            msgs.append({
                "en": "Strong winds expected - delay spraying to avoid drift.",
                "hi": "Tez hawa chalne ki sambhavna - spray karne mein deri karein.",
            })
        if not msgs:
            msgs.append({
                "en": "Normal conditions - routine farm activity can continue.",
                "hi": "Samanya mausam - roz ka kaam jaari rakh sakte hain.",
            })

        advisories.append({
            "date": day["date"],
            "temp_max": round(day["temp_max"], 1),
            "temp_min": round(day["temp_min"], 1),
            "rain_mm": round(day["rain"], 1),
            "messages": [m.get(lang, m["en"]) for m in msgs],
        })

    return advisories