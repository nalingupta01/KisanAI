"""
KisanAI - Crop Reference Data
-------------------------------
This is the "knowledge base" for the Crop Calendar and Fertilizer
Calculator modules. No AI/ML needed - this is curated static data,
which is exactly how real agri-advisory tools like this work at
a small scale. Add more crops/months any time by editing these dicts.
"""

# Month-by-month advisory for common crops (Hinglish, matches farmer's real speech)
CROP_CALENDAR = {
    "Wheat (Gehu)": {
        "November": "Sowing time - prepare field, first irrigation before sowing.",
        "December": "First urea dose after 21 days of sowing. Watch for aphids.",
        "January": "Second urea dose. Irrigate every 18-21 days.",
        "February": "Watch for yellow rust - spray fungicide if leaves show yellow streaks.",
        "March": "Grain filling stage - avoid water stress. Stop irrigation before harvest.",
        "April": "Harvest when grain moisture is below 14%.",
    },
    "Rice (Dhan)": {
        "June": "Nursery preparation and sowing (Kharif season begins).",
        "July": "Transplanting. Maintain 2-3 inch standing water.",
        "August": "Watch for stem borer and leaf folder. Apply second dose of nitrogen.",
        "September": "Flowering stage - do not let field dry out.",
        "October": "Grain maturity - drain field 10 days before harvest.",
        "November": "Harvest when 80% grains turn golden.",
    },
    "Cotton (Karpas)": {
        "May": "Land preparation, sowing with pre-monsoon showers.",
        "June": "Thinning and gap filling. First fertilizer dose.",
        "July": "Watch for bollworm - install pheromone traps.",
        "August": "Flowering and boll formation - critical irrigation period.",
        "September": "Pest monitoring continues, especially pink bollworm.",
        "October": "First picking begins.",
    },
    "Mustard (Sarson)": {
        "October": "Sowing time after monsoon retreat.",
        "November": "First irrigation and thinning.",
        "December": "Watch for aphid attack - spray neem oil if seen.",
        "January": "Pod formation stage - irrigate if needed.",
        "February": "Harvest when pods turn yellow-brown.",
    },
    "Tomato (Tamatar)": {
        "June": "Nursery sowing for Kharif crop.",
        "July": "Transplanting to main field.",
        "August": "Staking plants, watch for blight in humid weather.",
        "September": "Flowering and fruiting - regular irrigation needed.",
        "October": "Harvesting begins, continues for 6-8 weeks.",
    },
    "Onion (Pyaz)": {
        "October": "Nursery sowing.",
        "November": "Transplanting seedlings to field.",
        "December": "Weeding and first fertilizer top dressing.",
        "January": "Bulb development stage - avoid excess nitrogen.",
        "February": "Stop irrigation as neck falls over.",
        "March": "Harvest when 50% of tops fall over naturally.",
    },
    "Potato (Aloo)": {
        "October": "Land preparation and planting.",
        "November": "Earthing up after 25-30 days.",
        "December": "Watch for late blight in foggy weather - preventive spray.",
        "January": "Tuber bulking stage - maintain soil moisture.",
        "February": "Stop irrigation 10 days before harvest.",
    },
    "Maize (Makka)": {
        "June": "Sowing with onset of monsoon.",
        "July": "First weeding and nitrogen top dressing.",
        "August": "Tasseling stage - critical for irrigation.",
        "September": "Cob filling stage.",
        "October": "Harvest when husk turns brown and dry.",
    },
    "Chickpea (Chana)": {
        "October": "Sowing time (Rabi season).",
        "November": "Light irrigation if no rainfall.",
        "December": "Watch for pod borer - install pheromone traps.",
        "January": "Flowering and pod formation.",
        "February": "Harvest when plants turn yellow-brown.",
    },
    "Sugarcane (Ganna)": {
        "February": "Planting time (spring season).",
        "April": "Earthing up and gap filling.",
        "July": "Peak growth stage - heavy irrigation and nitrogen needed.",
        "October": "Reduce irrigation as maturity approaches.",
        "December": "Harvesting season begins.",
    },
    "Groundnut (Mungfali)": {
        "June": "Sowing time with onset of monsoon.",
        "July": "First weeding, gypsum application at flowering.",
        "August": "Pegging stage - keep soil loose, earth up around plants.",
        "September": "Pod development - avoid water stress.",
        "October": "Harvest when leaves turn yellow and pods show netting.",
    },
    "Soybean (Soyabean)": {
        "June": "Sowing with first good monsoon rain.",
        "July": "Weeding and gap filling within 20-25 days.",
        "August": "Flowering and pod formation - critical irrigation stage.",
        "September": "Pod filling - watch for pod borer.",
        "October": "Harvest when 95% pods turn brown.",
    },
    "Bajra (Pearl Millet)": {
        "June": "Sowing time with monsoon onset.",
        "July": "Thinning and first weeding.",
        "August": "Earhead emergence - top dress with nitrogen.",
        "September": "Grain filling stage.",
        "October": "Harvest when grains are hard and moisture is low.",
    },
    "Jowar (Sorghum)": {
        "June": "Sowing time (Kharif) with monsoon.",
        "July": "Thinning, first weeding, nitrogen top dressing.",
        "August": "Watch for shoot fly and stem borer.",
        "September": "Earhead formation stage.",
        "October": "Harvest when grains are hard.",
    },
    "Chilli (Mirchi)": {
        "June": "Nursery sowing.",
        "July": "Transplanting to main field.",
        "August": "Flowering begins - watch for thrips and mites.",
        "September": "First picking of green chillies.",
        "October": "Continued picking every 10-15 days.",
        "November": "Final pickings, can leave for red chilli drying.",
    },
}

# Fertilizer requirement per ACRE (kg). Land size entered in other units
# gets converted to acres before applying these numbers.
# Figures are commonly-used general recommendations for demo purposes -
# always mention in your report that real farmers should confirm with a
# local Krishi Vigyan Kendra / soil test before actual application.
FERTILIZER_PER_ACRE = {
    "Wheat (Gehu)":     {"Urea": 55, "DAP": 45, "MOP": 20},
    "Rice (Dhan)":      {"Urea": 60, "DAP": 40, "MOP": 25},
    "Cotton (Karpas)":  {"Urea": 50, "DAP": 35, "MOP": 20},
    "Mustard (Sarson)": {"Urea": 35, "DAP": 30, "MOP": 15},
    "Tomato (Tamatar)": {"Urea": 45, "DAP": 50, "MOP": 30},
    "Onion (Pyaz)":     {"Urea": 45, "DAP": 40, "MOP": 25},
    "Potato (Aloo)":    {"Urea": 60, "DAP": 60, "MOP": 40},
    "Maize (Makka)":    {"Urea": 50, "DAP": 35, "MOP": 20},
    "Chickpea (Chana)": {"Urea": 15, "DAP": 40, "MOP": 15},
    "Sugarcane (Ganna)": {"Urea": 90, "DAP": 55, "MOP": 40},
    "Groundnut (Mungfali)": {"Urea": 20, "DAP": 50, "MOP": 25},
    "Soybean (Soyabean)":   {"Urea": 20, "DAP": 45, "MOP": 20},
    "Bajra (Pearl Millet)": {"Urea": 40, "DAP": 25, "MOP": 15},
    "Jowar (Sorghum)":      {"Urea": 40, "DAP": 25, "MOP": 15},
    "Chilli (Mirchi)":      {"Urea": 50, "DAP": 55, "MOP": 35},
    "Turmeric (Haldi)":     {"Urea": 45, "DAP": 60, "MOP": 60},
}

# Prices per kg (INR). Unlike mandi prices, fertilizer prices in India are
# NOT freely market-traded - Urea, DAP, and MOP retail rates are fixed by
# the Government of India under the Nutrient Based Subsidy (NBS) scheme,
# so there is no "live market API" to plug in here the way there is for
# mandi prices. These figures are the official 2026 MRPs (Rabi/Kharif
# season) as fixed by the Dept. of Fertilizers - they only change when
# the government revises the subsidy, typically once or twice a year.
# Source figures (per 50kg bag, converted to per-kg below):
#   Urea: Rs 266/bag  ->  Rs 5.32/kg
#   DAP:  Rs 1350/bag ->  Rs 27.00/kg
#   MOP:  Rs 1710.54/bag -> Rs 34.21/kg
# To keep this current: check https://www.dbtfert.nic.in or search
# "DAP MOP Urea MRP" each season and update the numbers below.
FERTILIZER_PRICE_PER_KG = {
    "Urea": 5.32,
    "DAP": 27.00,
    "MOP": 34.21,
}

# Conversion factors to acres
LAND_UNIT_TO_ACRE = {
    "Acre": 1.0,
    "Hectare": 2.471,
    "Bigha (Rajasthan, ~0.625 acre)": 0.625,
}