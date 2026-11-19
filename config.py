"""
KisanAI - API key configuration (safe to publish: contains NO real keys)
-----------------------------------------------------------------------
Keys are read from environment variables. Never write real keys in this file.

Local run   : set environment variables (or a local .env you do NOT commit).
Streamlit Cloud : App -> Settings -> Secrets (top-level secrets are exposed
                  to the app as environment variables), e.g.

    OPENWEATHER_API_KEY = "..."
    PLANT_ID_API_KEY    = "..."
    ADMIN_PASSWORD      = "choose-a-strong-password"

Features whose keys are missing show a friendly warning instead of crashing.
"""

import os

# OpenWeatherMap (weather advisory) - https://openweathermap.org/api
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "PASTE_YOUR_OPENWEATHER_KEY_HERE")

# Plant.id (crop disease detection) - https://web.plant.id/
PLANT_ID_API_KEY = os.getenv("PLANT_ID_API_KEY", "PASTE_YOUR_PLANT_ID_KEY_HERE")

# Twilio (optional SMS alerts) - https://www.twilio.com/try-twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "PASTE_YOUR_TWILIO_SID_HERE")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "PASTE_YOUR_TWILIO_TOKEN_HERE")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
TWILIO_MESSAGING_SERVICE_SID = os.getenv("TWILIO_MESSAGING_SERVICE_SID", "PASTE_YOUR_MESSAGING_SERVICE_SID_HERE")

# Admin page password. Empty = admin login disabled.
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
