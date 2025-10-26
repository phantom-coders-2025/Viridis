# app/business.py

EMISSION_FACTORS = {
    "electricity": 0.82,        # kg CO2e per kWh
    "diesel": 2.68,             # kg CO2e per liter
    "biomedical_incinerated": 2.5, # kg CO2e per kg waste
    "biomedical_autoclaved": 0.8,  # kg CO2e per kg waste
    "water": 0.0003,            # kg CO2e per L water
    # Add more as needed
}

def calculate_co2e(category: str, quantity: float, subcategory: str = "") -> float:
    key = category
    # combine with subcategory if relevant
    if category == "biomedical":
        key = f"biomedical_{subcategory.lower()}"
    factor = EMISSION_FACTORS.get(key, 0)
    return round(quantity * factor, 4)

def calculate_sustainability_score(
    epi: float,                  # Energy Performance Index: kWh/bed/year
    waste_segregation: float,    # fraction 0-1
    renewable_pct: float,        # 0-1 if renewable energy is present
    emission_trend: float        # percent decrease (+ is good, - is bad)
) -> str:
    # Weighting: EPI (40%), Waste Segregation (25%), Renewables (20%), Trend (15%)
    epi_score = min(100, max(0, 100 - epi))            # Lower EPI = better
    waste_score = waste_segregation * 100
    renewable_score = renewable_pct * 100
    trend_score = max(0, min(100, emission_trend))
    final = (
        epi_score * 0.4 +
        waste_score * 0.25 +
        renewable_score * 0.2 +
        trend_score * 0.15
    )
    # Grade
    if final >= 90: return "A+"
    elif final >= 80: return "A"
    elif final >= 70: return "B+"
    elif final >= 60: return "B"
    elif final >= 50: return "C"
    elif final >= 40: return "D"
    else: return "F"
