# 🌾 KisanAI: AI-Powered Crop Advisory Platform for Farmers

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57)

A bilingual (English/Hindi) web application that gives Indian farmers simple, actionable advice: weather-based alerts, crop disease detection from a leaf photo, fertilizer planning, mandi prices and SMS alerts for farmers without smartphones.

**🔗 Live demo:** _add your Streamlit link here_

<!-- After uploading screenshots to a `screenshots/` folder, remove the arrows on the next line to show them:
![Home](screenshots/home.png)
-->

## 📌 Overview

Many farmers make decisions on weather, inputs and selling prices without timely, easy-to-understand information. KisanAI brings these into one app that works in **English and Hindi**, keeps a profile for each farmer, and can send the most important weather alert by **SMS**.

## ✨ Features

| Module | What it does |
|---|---|
| **Farmer profile** | Registers farmers (name, mobile, state, district, crop, land size, language) in SQLite |
| **Weather advisory** | Reads a 5-day OpenWeatherMap forecast and applies explainable rules to alert for rain, heat stress, frost, high humidity and strong wind |
| **Disease detector** | Identifies crop diseases from a leaf photo using the Plant.id computer-vision API and saves the diagnosis history |
| **SMS alerts** | Sends the weather advisory to a farmer's phone through Twilio |
| **Crop calendar** | Sowing, care and harvest guidance for 15 crops |
| **Fertilizer calculator** | Converts land size (acre/hectare/bigha etc.) into fertilizer quantity and estimated cost |
| **Mandi price tracker** | Looks up crop prices by state and district from a CSV dataset (sample data for 13 states) |
| **Admin dashboard** | Password-protected view of registered farmers with Pandas-driven charts by crop and state |
| **Bilingual UI** | One-click switch between English and Hindi |

## 🧠 How it works

```
 Farmer (Streamlit UI, English / Hindi)
        │
        ├── Profile ───────────────► SQLite (farmers, diagnosis history)
        ├── Weather advisory ──────► OpenWeatherMap API ─► rule engine ─► alerts ─► Twilio SMS
        ├── Disease detector ──────► Plant.id API ─► diagnosis + confidence
        ├── Calendar / Fertilizer ─► crop_data.py reference tables
        └── Mandi prices ──────────► mandi_prices.csv (Pandas)
```

The weather advisory is a **rule-based engine**: it summarises the forecast per day (max/min temperature, rain, humidity, wind) and applies simple thresholds, so every alert is easy to explain.

## 🛠️ Tech stack

Python · Streamlit · SQLite · Pandas · REST APIs (OpenWeatherMap, Plant.id, Twilio)

## 📁 Project structure

```
app.py            Streamlit UI (entry point)
config.py         API keys read from environment variables (no secrets in code)
database.py       SQLite setup, farmer and diagnosis functions
translations.py   English / Hindi text
crop_data.py      Crop calendar and fertilizer reference data
weather.py        OpenWeatherMap integration and advisory rules
disease.py        Plant.id integration
sms.py            Twilio SMS alerts
mandi.py          Mandi price lookup (reads mandi_prices.csv)
fertilizer.py     Fertilizer calculation logic
mandi_prices.csv  Sample mandi price data
```

## 🚀 Run locally

```bash
git clone https://github.com/nalingupta01/KisanAI.git
cd KisanAI
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`. The SQLite database is created automatically on first run.

## 🔑 API keys

Keys are read from environment variables, never stored in the code. Features without a key show a warning instead of failing.

| Variable | Needed for | Get it from |
|---|---|---|
| `OPENWEATHER_API_KEY` | Weather advisory | openweathermap.org/api |
| `PLANT_ID_API_KEY` | Disease detector | web.plant.id |
| `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER` | SMS alerts (optional) | twilio.com |
| `ADMIN_PASSWORD` | Admin page (empty = disabled) | choose your own |

On Windows PowerShell: `$env:OPENWEATHER_API_KEY="your_key"` before running the app.

## ☁️ Deploy on Streamlit Community Cloud

1. Push the repo to GitHub (public).
2. On share.streamlit.io choose **Create app**, select this repo, branch `main`, main file `app.py`.
3. Add your keys in **Settings → Secrets**, for example:
   ```toml
   OPENWEATHER_API_KEY = "your_key"
   PLANT_ID_API_KEY = "your_key"
   ADMIN_PASSWORD = "your_password"
   ```

## ⚠️ Limitations

- Mandi prices come from a sample CSV. Replace `mandi_prices.csv` with a fresh download from data.gov.in for current prices.
- Fertilizer quantities are general reference figures. Confirm with a soil test or the local Krishi Vigyan Kendra before real use.
- Twilio trial accounts can only text verified numbers.
- On free cloud hosting the SQLite file resets when the app restarts.

## 🔮 Future scope

- Live mandi price feed and more crops/regions
- Real SMS delivery to unverified numbers (paid Twilio plan)
- Multi-role admin access with edit/delete controls
- Regional languages beyond Hindi and English

## 👤 Author

**Nalin Gupta** 
[GitHub](https://github.com/nalingupta01) · [LinkedIn](https://linkedin.com/in/guptanalin)
