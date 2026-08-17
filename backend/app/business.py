# app/business.py
from typing import Any, Dict, List, Tuple

# Comprehensive GHG Protocol Emission Factors (kg CO2e per unit)
EMISSION_FACTORS: Dict[str, float] = {
    # Scope 1 - Direct Fuel & Stationary/Mobile Combustion
    "diesel": 2.68,                      # kg CO2e per liter (DG set power generation)
    "gas": 2.02,                         # kg CO2e per m3 (PNG / LPG Boilers & Kitchen)
    "lpg": 2.98,                         # kg CO2e per kg
    "petrol": 2.31,                      # kg CO2e per liter (Ambulances & fleet)
    # Scope 1 - Medical Anesthetic Gases (GWP-weighted)
    "anesthetic": 130.0,                 # default general anesthetic factor
    "anesthetic_desflurane": 2540.0,     # kg CO2e per kg (High GWP = 2,540)
    "anesthetic_isoflurane": 510.0,      # kg CO2e per kg (GWP = 510)
    "anesthetic_sevoflurane": 130.0,     # kg CO2e per kg (GWP = 130)
    "anesthetic_nitrous_oxide": 298.0,   # kg CO2e per kg (N2O GWP = 298)
    "anesthetic_n2o": 298.0,
    # Scope 2 - Purchased Energy & Electricity
    "electricity": 0.82,                 # kg CO2e per kWh (CEA Grid Average)
    "electricity_grid": 0.82,            # kg CO2e per kWh
    "electricity_solar": 0.0,            # Clean offset
    "steam": 0.18,                       # kg CO2e per kg steam
    # Scope 3 - Bio-Medical Waste (CPCB Bio-Medical Waste Management Rules 2016)
    "biomedical": 2.0,                   # default general biomedical waste
    "biomedical_yellow": 2.85,           # Yellow Bag (Incineration): anatomical, soiled waste
    "biomedical_incinerated": 2.85,
    "biomedical_red": 0.72,              # Red Bag (Autoclaving + Shredding): contaminated plastic
    "biomedical_autoclaved": 0.72,
    "biomedical_blue": 0.45,             # Blue Bag (Disinfection + Glass recycling): vials, ampoules
    "biomedical_glass": 0.45,
    "biomedical_white": 0.60,            # White Translucent (Needles / Sharps encapsulation)
    "biomedical_sharps": 0.60,
    "waste_general": 0.95,               # Municipal solid waste (landfill / composting)
    # Scope 3 - Water & Supply Chain
    "water": 0.00034,                    # kg CO2e per Liter (municipal treatment & pumping)
    "water_recycled": 0.00010,           # kg CO2e per Liter (STP treated greywater)
    "supply_chain": 1.20,                # kg CO2e per procurement unit
}


def determine_ghg_scope(category: str, subcategory: str = "") -> str:
    """Categorizes an emission activity into Scope 1, Scope 2, or Scope 3."""
    cat = (category or "").strip().lower()
    sub = (subcategory or "").strip().lower()

    # Scope 1: Direct Combustion & Anesthetic Gases
    if cat in {"diesel", "gas", "lpg", "petrol", "anesthetic", "fuel"} or "anesthetic" in cat or "anesthetic" in sub:
        return "Scope 1"

    # Scope 2: Purchased Electricity, Steam, Chilled Water
    if cat in {"electricity", "power", "grid", "steam", "cooling"}:
        return "Scope 2"

    # Scope 3: Bio-Medical Waste, General Waste, Water, Procurement
    return "Scope 3"


def get_emission_factor(category: str, subcategory: str = "") -> float:
    """Resolves the precise emission factor based on category and subcategory."""
    cat_lower = (category or "").strip().lower()
    sub_lower = (subcategory or "").strip().lower()

    # Try combined specific key
    if sub_lower:
        combined_key = f"{cat_lower}_{sub_lower}"
        if combined_key in EMISSION_FACTORS:
            return EMISSION_FACTORS[combined_key]

        if cat_lower == "anesthetic" and f"anesthetic_{sub_lower}" in EMISSION_FACTORS:
            return EMISSION_FACTORS[f"anesthetic_{sub_lower}"]

        if cat_lower == "biomedical" and f"biomedical_{sub_lower}" in EMISSION_FACTORS:
            return EMISSION_FACTORS[f"biomedical_{sub_lower}"]

    # Fallback to category key
    return EMISSION_FACTORS.get(cat_lower, 1.0)


def calculate_co2e(category: str, quantity: float, subcategory: str = "") -> float:
    """Calculates total kg CO2e for an emission entry."""
    factor = get_emission_factor(category, subcategory)
    return round(float(quantity) * factor, 4)


def calculate_sustainability_score(
    epi: float,                  # Energy Performance Index: kWh/bed/year
    waste_segregation: float,    # fraction 0-1
    renewable_pct: float,        # fraction 0-1
    emission_trend: float,       # percent decrease (+ is improvement, - is increase)
    scope1_ratio: float = 0.2,   # ratio of direct emissions
) -> Tuple[str, int, List[Dict[str, str]]]:
    """Calculates composite Hospital Sustainability Score (0-100) & actionable insights."""
    # Benchmark targets: Target EPI = 30-40 kWh/bed/day (or normalized annual target)
    epi_score = min(100.0, max(0.0, 100.0 - (epi / 8.0 if epi > 60 else epi * 0.8)))
    waste_score = min(100.0, max(0.0, waste_segregation * 100.0))
    renewable_score = min(100.0, max(0.0, renewable_pct * 100.0))
    trend_score = min(100.0, max(0.0, 50.0 + (emission_trend * 2.5)))

    # Weighted scoring formula: EPI (35%), Waste (25%), Renewables (25%), Trend (15%)
    final_numeric = round(
        (epi_score * 0.35) +
        (waste_score * 0.25) +
        (renewable_score * 0.25) +
        (trend_score * 0.15)
    )
    final_score = int(min(100, max(0, final_numeric)))

    if final_score >= 90:
        grade = "A+ (Exemplary Green Hospital)"
    elif final_score >= 80:
        grade = "A (NABH Green Certified)"
    elif final_score >= 70:
        grade = "B+ (Compliant & Transitioning)"
    elif final_score >= 60:
        grade = "B (Moderate Footprint)"
    elif final_score >= 50:
        grade = "C (Needs Optimization)"
    elif final_score >= 40:
        grade = "D (Sub-Standard)"
    else:
        grade = "F (Critical Carbon Exposure)"

    recommendations: List[Dict[str, str]] = []
    if renewable_pct < 0.25:
        recommendations.append({
            "type": "renewable",
            "title": "Install Captive Solar Rooftop System",
            "desc": f"Facility currently draws {round((1-renewable_pct)*100, 1)}% from grid. A 150 kWp solar PV array can abate ~150,000 kg CO2e/year and save ~₹12.5L annually.",
            "impact": "High Impact",
        })
    if waste_segregation < 0.75:
        recommendations.append({
            "type": "waste",
            "title": "CPCB Bio-Medical Waste Red/Yellow Segregation",
            "desc": f"Segregation efficiency is {round(waste_segregation * 100, 1)}%. Diverting uncontaminated plastics to autoclave vs incineration reduces waste emissions by 74%.",
            "impact": "High Impact",
        })
    if epi > 45:
        recommendations.append({
            "type": "energy",
            "title": "HVAC Variable Refrigerant Flow & VFD Retrofitting",
            "desc": f"Energy intensity is elevated at {round(epi, 1)} kWh/bed. VFD installations on chilled water pumps can cut energy consumption by 18%.",
            "impact": "Quick Win",
        })
    if not recommendations:
        recommendations.append({
            "type": "maintenance",
            "title": "Maintain NABH Green OT Protocol",
            "desc": "Hospital operations demonstrate premier energy and waste metrics. Conduct bi-annual audit verifications to retain leadership tier.",
            "impact": "Ongoing",
        })

    return grade, final_score, recommendations


def calculate_whatif_simulation(
    baseline_annual_co2e: float,
    baseline_electricity_kwh: float,
    baseline_waste_kg: float,
    solar_capacity_kw: float,
    led_retrofit_pct: float,
    anesthetic_switch_pct: float,
    waste_autoclave_pct: float,
    electricity_tariff_inr: float = 8.5,
) -> Dict[str, Any]:
    """Calculates carbon reduction, cost savings, and financial payback for sustainability investments."""
    # 1. Solar Generation: ~1,400 kWh generated per kWp installed in India annually
    annual_solar_gen_kwh = solar_capacity_kw * 1400.0
    solar_co2e_cut = annual_solar_gen_kwh * EMISSION_FACTORS["electricity"]
    solar_savings_inr = annual_solar_gen_kwh * electricity_tariff_inr
    solar_capex_inr = solar_capacity_kw * 45000.0  # Approx ₹45,000 per kWp

    # 2. LED Retrofit: Lighting accounts for ~20% of hospital power; LED reduces lighting load by 40%
    lighting_baseline_kwh = baseline_electricity_kwh * 0.20
    led_kwh_saved = lighting_baseline_kwh * (led_retrofit_pct / 100.0) * 0.40
    led_co2e_cut = led_kwh_saved * EMISSION_FACTORS["electricity"]
    led_savings_inr = led_kwh_saved * electricity_tariff_inr
    led_capex_inr = (baseline_electricity_kwh / 1000.0) * (led_retrofit_pct / 100.0) * 8000.0

    # 3. Anesthetic Switch: Shifting from Desflurane to Sevoflurane saves ~2,410 kg CO2e per kg of agent
    anesthetic_co2e_cut = (baseline_annual_co2e * 0.08) * (anesthetic_switch_pct / 100.0) * 0.85
    anesthetic_savings_inr = (anesthetic_switch_pct / 100.0) * 85000.0  # Drug acquisition differential
    anesthetic_capex_inr = 0.0  # Protocol change, negligible capex

    # 4. Waste Autoclave: Yellow (incinerated @ 2.85) to Red (autoclaved @ 0.72) -> Delta = 2.13 kg CO2e/kg
    waste_diverted_kg = (baseline_waste_kg * 0.35) * (waste_autoclave_pct / 100.0)
    waste_co2e_cut = waste_diverted_kg * 2.13
    waste_savings_inr = waste_diverted_kg * 12.0  # Treatment tariff difference
    waste_capex_inr = 250000.0 if waste_autoclave_pct > 30 else 50000.0

    total_co2e_reduction = round(solar_co2e_cut + led_co2e_cut + anesthetic_co2e_cut + waste_co2e_cut, 2)
    total_annual_savings = round(solar_savings_inr + led_savings_inr + anesthetic_savings_inr + waste_savings_inr, 2)
    total_capex = round(solar_capex_inr + led_capex_inr + anesthetic_capex_inr + waste_capex_inr, 2)
    monthly_savings = round(total_annual_savings / 12.0, 2)

    payback_years = round(total_capex / total_annual_savings, 2) if total_annual_savings > 0 else 0.0
    projected_co2e = max(0.0, round(baseline_annual_co2e - total_co2e_reduction, 2))
    reduction_pct = round((total_co2e_reduction / baseline_annual_co2e * 100.0), 1) if baseline_annual_co2e > 0 else 0.0

    breakdown = [
        {"measure": "Rooftop Solar PV", "capex_inr": round(solar_capex_inr, 2), "annual_savings_inr": round(solar_savings_inr, 2), "co2e_cut_kg": round(solar_co2e_cut, 2)},
        {"measure": "LED & Smart Controls", "capex_inr": round(led_capex_inr, 2), "annual_savings_inr": round(led_savings_inr, 2), "co2e_cut_kg": round(led_co2e_cut, 2)},
        {"measure": "Green Anesthesia (Sevoflurane/TIVA)", "capex_inr": round(anesthetic_capex_inr, 2), "annual_savings_inr": round(anesthetic_savings_inr, 2), "co2e_cut_kg": round(anesthetic_co2e_cut, 2)},
        {"measure": "BMW Autoclaving Diversion", "capex_inr": round(waste_capex_inr, 2), "annual_savings_inr": round(waste_savings_inr, 2), "co2e_cut_kg": round(waste_co2e_cut, 2)},
    ]

    return {
        "baseline_annual_co2e_kg": baseline_annual_co2e,
        "projected_annual_co2e_kg": projected_co2e,
        "co2e_reduction_kg": total_co2e_reduction,
        "co2e_reduction_pct": reduction_pct,
        "monthly_savings_inr": monthly_savings,
        "annual_savings_inr": total_annual_savings,
        "estimated_capex_inr": total_capex,
        "payback_years": payback_years,
        "scope1_reduction_kg": round(anesthetic_co2e_cut, 2),
        "scope2_reduction_kg": round(solar_co2e_cut + led_co2e_cut, 2),
        "scope3_reduction_kg": round(waste_co2e_cut, 2),
        "roi_breakdown": breakdown,
    }

