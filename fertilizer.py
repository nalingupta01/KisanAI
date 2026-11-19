"""
KisanAI - Fertilizer & Pesticide Calculator
----------------------------------------------
Pure arithmetic - no external API needed. Converts the farmer's land
size into acres, looks up the per-acre requirement, and scales it.
"""

from crop_data import FERTILIZER_PER_ACRE, FERTILIZER_PRICE_PER_KG, LAND_UNIT_TO_ACRE


def calculate_fertilizer(crop, land_size, land_unit):
    """
    Returns a dict: {fertilizer_name: {"kg": x, "cost": y}} plus a "total_cost" key.
    """
    if crop not in FERTILIZER_PER_ACRE:
        return None

    acres = land_size * LAND_UNIT_TO_ACRE.get(land_unit, 1.0)
    per_acre = FERTILIZER_PER_ACRE[crop]

    result = {}
    total_cost = 0.0
    for fert, kg_per_acre in per_acre.items():
        kg_needed = round(kg_per_acre * acres, 1)
        cost = round(kg_needed * FERTILIZER_PRICE_PER_KG[fert], 0)
        result[fert] = {"kg": kg_needed, "cost": cost}
        total_cost += cost

    result["total_cost"] = round(total_cost, 0)
    result["acres"] = round(acres, 2)
    return result