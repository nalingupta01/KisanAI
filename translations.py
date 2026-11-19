"""
KisanAI - Translations
------------------------
Simple dictionary-based translation. No external library needed.
Add more keys as you add more screens.
"""

TEXTS = {
    "app_title":        {"en": "KisanAI - Smart Crop Advisory", "hi": "KisanAI - स्मार्ट फसल सलाहकार"},
    "welcome":           {"en": "Welcome, Farmer!", "hi": "स्वागत है, किसान भाई!"},
    "nav_profile":       {"en": "My Profile", "hi": "मेरी प्रोफ़ाइल"},
    "nav_weather":       {"en": "Weather Advisory", "hi": "मौसम सलाह"},
    "nav_mandi":         {"en": "Mandi Prices", "hi": "मंडी भाव"},
    "nav_calendar":      {"en": "Crop Calendar", "hi": "फसल कैलेंडर"},
    "nav_fertilizer":    {"en": "Fertilizer Calculator", "hi": "खाद कैलकुलेटर"},
    "nav_disease":       {"en": "Disease Detector", "hi": "रोग पहचान"},
    "name":              {"en": "Full Name", "hi": "पूरा नाम"},
    "mobile":            {"en": "Mobile Number", "hi": "मोबाइल नंबर"},
    "state":             {"en": "State", "hi": "राज्य"},
    "district":          {"en": "District", "hi": "जिला"},
    "crop":              {"en": "Main Crop", "hi": "मुख्य फसल"},
    "land_size":         {"en": "Land Size", "hi": "भूमि का आकार"},
    "land_unit":         {"en": "Unit", "hi": "इकाई"},
    "save_profile":      {"en": "Save Profile", "hi": "प्रोफ़ाइल सहेजें"},
    "profile_saved":     {"en": "Profile saved successfully!", "hi": "प्रोफ़ाइल सफलतापूर्वक सहेजी गई!"},
    "enter_city":        {"en": "Enter your city/district", "hi": "अपना शहर/जिला दर्ज करें"},
    "get_advisory":      {"en": "Get Advisory", "hi": "सलाह प्राप्त करें"},
    "select_crop":       {"en": "Select Crop", "hi": "फसल चुनें"},
    "select_state":      {"en": "Select State", "hi": "राज्य चुनें"},
    "check_prices":      {"en": "Check Prices", "hi": "भाव देखें"},
    "select_month":      {"en": "Select Month", "hi": "महीना चुनें"},
    "calculate":         {"en": "Calculate", "hi": "गणना करें"},
    "upload_leaf":       {"en": "Upload a photo of the affected leaf", "hi": "प्रभावित पत्ती की फोटो अपलोड करें"},
    "diagnose":          {"en": "Diagnose", "hi": "जाँच करें"},
}


def t(key, lang="en"):
    """Return translated text for a key. Falls back to English, then the key itself."""
    entry = TEXTS.get(key, {})
    return entry.get(lang, entry.get("en", key))