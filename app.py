"""
KisanAI - Main App
--------------------
Run with:  streamlit run app.py

This single file wires together all the modules. Each module's real
logic lives in its own file (weather.py, mandi.py, fertilizer.py,
disease.py) - this file is just the UI/navigation layer.
"""

import streamlit as st
import pandas as pd

import config
import database as db
from translations import t
from crop_data import CROP_CALENDAR, FERTILIZER_PER_ACRE, LAND_UNIT_TO_ACRE
import weather
import mandi
import fertilizer
import disease
import sms

# ---------- App setup ----------
st.set_page_config(page_title="KisanAI", page_icon="🌾", layout="centered")
db.init_db()

if "farmer" not in st.session_state:
    st.session_state.farmer = None
if "lang" not in st.session_state:
    st.session_state.lang = "en"

lang = st.session_state.lang

# ---------- Sidebar: language + navigation ----------
st.sidebar.title("🌾 KisanAI")
lang_choice = st.sidebar.radio("Language / भाषा", ["English", "हिंदी"], horizontal=True)
st.session_state.lang = "hi" if lang_choice == "हिंदी" else "en"
lang = st.session_state.lang

page = st.sidebar.radio(
    "Menu",
    [
        t("nav_profile", lang),
        t("nav_weather", lang),
        t("nav_mandi", lang),
        t("nav_calendar", lang),
        t("nav_fertilizer", lang),
        t("nav_disease", lang),
        t("nav_admin", lang),
    ],
)

st.title(t("app_title", lang))

# ================================================================
# PAGE 1: Farmer Profile
# ================================================================
if page == t("nav_profile", lang):
    st.header(t("nav_profile", lang))

    existing_mobile = st.text_input(t("mobile", lang), key="lookup_mobile")
    if existing_mobile:
        found = db.get_farmer_by_mobile(existing_mobile)
        if found:
            st.session_state.farmer = found
            st.success(f"{t('welcome', lang)} {found['name']}")

    with st.form("profile_form"):
        name = st.text_input(t("name", lang))
        mobile = st.text_input(t("mobile", lang) + " (new)")
        state = st.selectbox(t("state", lang), mandi.INDIAN_STATES)
        district = st.text_input(t("district", lang))
        crop = st.selectbox(t("crop", lang), list(CROP_CALENDAR.keys()))
        col1, col2 = st.columns(2)
        with col1:
            land_size = st.number_input(t("land_size", lang), min_value=0.0, step=0.1)
        with col2:
            land_unit = st.selectbox(t("land_unit", lang), list(LAND_UNIT_TO_ACRE.keys()))

        submitted = st.form_submit_button(t("save_profile", lang))
        if submitted:
            if not name or not mobile:
                st.error("Name and mobile number are required.")
            else:
                try:
                    farmer_id = db.add_farmer(name, mobile, state, district, crop, land_size, land_unit, lang)
                    st.session_state.farmer = db.get_farmer_by_mobile(mobile)
                    st.success(t("profile_saved", lang))
                except Exception as e:
                    st.error(f"Could not save (mobile number may already exist): {e}")

    if st.session_state.farmer:
        st.divider()
        st.subheader("Current profile")
        st.json(st.session_state.farmer)

# ================================================================
# PAGE 2: Weather Advisory
# ================================================================
elif page == t("nav_weather", lang):
    st.header(t("nav_weather", lang))

    default_city = st.session_state.farmer["district"] if st.session_state.farmer else ""
    city = st.text_input(t("enter_city", lang), value=default_city)

    if st.button(t("get_advisory", lang)) and city:
        if config.OPENWEATHER_API_KEY.startswith("PASTE_"):
            st.warning("Add your OpenWeatherMap API key in config.py first. See README.md Step 3.")
        else:
            with st.spinner("Fetching forecast..."):
                raw = weather.get_forecast(city, config.OPENWEATHER_API_KEY)
            if raw and "error" not in raw and raw.get("cod") == "200":
                summary = weather.summarize_forecast(raw)
                advisories = weather.generate_advisory(summary, lang)
                for day in advisories:
                    st.subheader(f"{day['date']}  |  {day['temp_min']}°C - {day['temp_max']}°C  |  Rain: {day['rain_mm']}mm")
                    for msg in day["messages"]:
                        st.info(msg)

                st.divider()
                st.caption("Optional: send today's advisory as SMS (requires Twilio setup - see sms.py)")
                sms_number = st.text_input("Farmer's mobile number (with +91)", value="+91")
                if st.button("Send SMS Alert"):
                    if config.TWILIO_ACCOUNT_SID.startswith("PASTE_"):
                        st.warning("Add your Twilio credentials in config.py first. See sms.py header.")
                    else:
                        text = sms.format_weather_alert_sms(advisories[0], lang)
                        ok, info = sms.send_sms_alert(
                            sms_number, text,
                            config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN,
                            from_number=config.TWILIO_FROM_NUMBER or None,
                            messaging_service_sid=config.TWILIO_MESSAGING_SERVICE_SID
                                if not config.TWILIO_MESSAGING_SERVICE_SID.startswith("PASTE_") else None,
                        )
                        st.success(f"SMS sent! (sid: {info})") if ok else st.error(f"Failed: {info}")
            else:
                st.error("Could not fetch weather. Check the city name or your API key.")

# ================================================================
# PAGE 3: Mandi Price Tracker
# ================================================================
elif page == t("nav_mandi", lang):
    st.header(t("nav_mandi", lang))

    col1, col2 = st.columns(2)
    with col1:
        state = st.selectbox(t("select_state", lang), mandi.INDIAN_STATES)
    with col2:
        commodity = st.selectbox(t("select_crop", lang), mandi.COMMON_COMMODITIES)

    if st.button(t("check_prices", lang)):
        df = mandi.get_mandi_prices(state=state, commodity=commodity)
        if df.empty:
            st.warning("No records found for that state/commodity combination. "
                       "Check that mandi_prices.csv exists in the project folder.")
        else:
            st.dataframe(df, use_container_width=True)
            st.caption("Prices shown are from mandi_prices.csv. Replace this file with a "
                       "fresh download from data.gov.in for live figures (see mandi.py header).")
            if "modal_price" in df.columns:
                chart_df = df[["market", "modal_price"]].copy()
                chart_df["modal_price"] = pd.to_numeric(chart_df["modal_price"], errors="coerce")
                st.bar_chart(chart_df.set_index("market"))

# ================================================================
# PAGE 4: Crop Calendar
# ================================================================
elif page == t("nav_calendar", lang):
    st.header(t("nav_calendar", lang))

    crop = st.selectbox(t("select_crop", lang), list(CROP_CALENDAR.keys()))
    calendar = CROP_CALENDAR[crop]
    month = st.selectbox(t("select_month", lang), list(calendar.keys()))

    st.info(calendar[month])

    st.divider()
    st.caption("Full year calendar for this crop:")
    for m, advice in calendar.items():
        st.write(f"**{m}**: {advice}")

# ================================================================
# PAGE 5: Fertilizer Calculator
# ================================================================
elif page == t("nav_fertilizer", lang):
    st.header(t("nav_fertilizer", lang))

    crop = st.selectbox(t("select_crop", lang), list(FERTILIZER_PER_ACRE.keys()))
    col1, col2 = st.columns(2)
    with col1:
        land_size = st.number_input(t("land_size", lang), min_value=0.1, value=1.0, step=0.1)
    with col2:
        land_unit = st.selectbox(t("land_unit", lang), list(LAND_UNIT_TO_ACRE.keys()))

    if st.button(t("calculate", lang)):
        result = fertilizer.calculate_fertilizer(crop, land_size, land_unit)
        if result:
            st.write(f"For **{result['acres']} acres** of {crop}:")
            for fert in ["Urea", "DAP", "MOP"]:
                st.write(f"- **{fert}**: {result[fert]['kg']} kg  (approx ₹{result[fert]['cost']:.0f})")
            st.success(f"Estimated total cost: ₹{result['total_cost']:.0f}")
        else:
            st.error("No fertilizer data available for this crop yet.")

# ================================================================
# PAGE 6: Disease Detector (optional / stretch)
# ================================================================
elif page == t("nav_disease", lang):
    st.header(t("nav_disease", lang))
    st.caption("Build this module last, after everything else works.")

    uploaded = st.file_uploader(t("upload_leaf", lang), type=["jpg", "jpeg", "png"])
    if uploaded:
        st.image(uploaded, width=300)

    if st.button(t("diagnose", lang)) and uploaded:
        if config.PLANT_ID_API_KEY.startswith("PASTE_"):
            st.warning("Add your Plant.id API key in config.py first. See README.md Step 3.")
        else:
            with st.spinner("Analyzing photo..."):
                result = disease.diagnose_leaf(uploaded.getvalue(), config.PLANT_ID_API_KEY)
            if "error" in result:
                st.error(f"Could not analyze image: {result['error']}")
            else:
                st.subheader(f"{result['disease']}  ({result['confidence']}% confidence)")
                st.info(disease.get_treatment_tip(result["disease"], lang))
                if st.session_state.farmer:
                    db.save_diagnosis(st.session_state.farmer["id"], result["disease"], result["confidence"])

# ================================================================
# PAGE 7: Admin (Krishi Adhikari view - password protected)
# ================================================================
elif page == t("nav_admin", lang):
    st.header(t("nav_admin", lang))

    if "admin_ok" not in st.session_state:
        st.session_state.admin_ok = False

    if not st.session_state.admin_ok:
        pw = st.text_input("Admin password", type="password")
        if st.button("Login"):
            if config.ADMIN_PASSWORD and pw == config.ADMIN_PASSWORD:
                st.session_state.admin_ok = True
                st.rerun()
            else:
                st.error("Wrong password.")
    else:
        farmers = db.get_all_farmers()
        st.write(f"**Total registered farmers: {len(farmers)}**")

        if farmers:
            df = pd.DataFrame(farmers)
            st.dataframe(df, use_container_width=True)

            st.divider()
            st.subheader("Farmers by crop")
            crop_counts = df["crop"].value_counts()
            st.bar_chart(crop_counts)

            st.divider()
            st.subheader("Farmers by state")
            state_counts = df["state"].value_counts()
            st.bar_chart(state_counts)

            st.divider()
            st.subheader("Diagnosis history lookup")
            selected_id = st.selectbox("Select farmer", df["id"].tolist(),
                                         format_func=lambda i: df[df["id"] == i]["name"].values[0])
            history = db.get_diagnosis_history(selected_id)
            if history:
                st.dataframe(pd.DataFrame(history), use_container_width=True)
            else:
                st.caption("No diagnosis history for this farmer.")
        else:
            st.info("No farmers registered yet.")

        if st.button("Logout"):
            st.session_state.admin_ok = False
            st.rerun()