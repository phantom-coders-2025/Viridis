# app/business.py
from typing import Dict, List, Tuple

EMISSION_FACTORS = {
    "electricity": 0.82,           # kg CO2e per kWh
    "diesel": 2.68,                # kg CO2e per liter
    "biomedical": 2.0,             # default kg CO2e per kg waste
    "biomedical_incinerated": 2.5, # kg CO2e per kg waste
    "biomedical_autoclaved": 0.8,  # kg CO2e per kg waste
    "water": 0.0003,               # kg CO2e per L water
    "gas": 2.02,                   # kg CO2e per m3
}


def get_emission_factor(category: str, subcategory: str = "") -> float:
    cat_lower = (category or "").strip().lower()
    sub_lower = (subcategory or "").strip().lower()

    if cat_lower == "biomedical" and sub_lower:
        key = f"biomedical_{sub_lower}"
        if key in EMISSION_FACTORS:
            return EMISSION_FACTORS[key]

    return EMISSION_FACTORS.get(cat_lower, 1.0)


def calculate_co2e(category: str, quantity: float, subcategory: str = "") -> float:
    factor = get_emission_factor(category, subcategory)
    return round(float(quantity) * factor, 4)


def calculate_sustainability_score(
    epi: float,                  # Energy Performance Index: kWh/bed/year
    waste_segregation: float,    # fraction 0-1
    renewable_pct: float,        # 0-1 if renewable energy is present
    emission_trend: float        # percent decrease (+ is good, - is bad)
) -> Tuple[str, int, List[Dict[str, str]]]:
    # Weighting: EPI (40%), Waste Segregation (25%), Renewables (20%), Trend (15%)
    epi_score = min(100.0, max(0.0, 100.0 - (epi / 10.0 if epi > 100 else epi)))
    waste_score = min(100.0, max(0.0, waste_segregation * 100.0))
    renewable_score = min(100.0, max(0.0, renewable_pct * 100.0))
    trend_score = min(100.0, max(0.0, 50.0 + (emission_trend * 2.5)))

    final_numeric = round(
        (epi_score * 0.40) +
        (waste_score * 0.25) +
        (renewable_score * 0.20) +
        (trend_score * 0.15)
    )
    final_score = int(min(100, max(0, final_numeric)))

    if final_score >= 90:
        grade = "A+"
    elif final_score >= 80:
        grade = "A"
    elif final_score >= 70:
        grade = "B+"
    elif final_score >= 60:
        grade = "B"
    elif final_score >= 50:
        grade = "C"
    elif final_score >= 40:
        grade = "D"
    else:
        grade = "F"

    # Contextual recommendations based on metrics
    recommendations: List[Dict[str, str]] = []
    if renewable_pct < 0.3:
        recommendations.append({
            "type": "renewable",
            "title": "Increase Renewable Energy Mix",
            "desc": f"Currently at {round(renewable_pct * 100, 1)}% renewable energy. Installing solar rooftop capacity could increase score by up to 15 points.",
            "impact": "High Impact"
        })
    if waste_segregation < 0.7:
        recommendations.append({
            "type": "waste",
            "title": "Enhance Biomedical Waste Segregation",
            "desc": f"Segregation rate is {round(waste_segregation * 100, 1)}%. Directing more non-hazardous waste away from incineration saves up to 1.7 kg CO2e/kg.",
            "impact": "High Impact"
        })
    if epi > 40:
        recommendations.append({
            "type": "energy",
            "title": "HVAC & Lighting Retrofitting",
            "desc": f"Energy index is {round(epi, 1)} kWh/bed. Smart thermostats and LED lighting can yield 10-20% efficiency gains.",
            "impact": "Quick Win"
        })
    if not recommendations:
        recommendations.append({
            "type": "maintenance",
            "title": "Maintain Sustainability Standards",
            "desc": "Facility operates with top-tier efficiency metrics. Continue monthly tracking and audit verifications.",
            "impact": "Ongoing"
        })

    return grade, final_score, recommendations
