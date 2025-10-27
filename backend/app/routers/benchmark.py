from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Hospital, Emission

@app.get("/benchmark-multi/{hospital_id}")
def benchmark_multi(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).get(hospital_id)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    beds = hospital.beds or 1

    # 1. Gather all peer hospitals (same type & similar beds)
    peer_query = db.query(Hospital).filter(
        Hospital.type == hospital.type,
        Hospital.beds >= beds - 50, Hospital.beds <= beds + 50,
        Hospital.id != hospital_id
    )
    peer_ids = [h.id for h in peer_query]

    def calc_epi(hosp_id, beds_):
        total_kwh = db.query(func.sum(Emission.quantity)).filter(
            Emission.hospital_id == hosp_id,
            Emission.category == "electricity"
        ).scalar() or 0
        return total_kwh / beds_

    def calc_emission_per_bed(hosp_id, beds_):
        total_co2e = db.query(func.sum(Emission.co2e)).filter(
            Emission.hospital_id == hosp_id
        ).scalar() or 0
        return total_co2e / beds_

    def calc_waste_per_bed(hosp_id, beds_):
        total_waste = db.query(func.sum(Emission.quantity)).filter(
            Emission.hospital_id == hosp_id,
            Emission.category == "biomedical"
        ).scalar() or 0
        return total_waste / beds_

    def calc_renewable_share(hosp_id):
        renewable = db.query(func.sum(Emission.quantity)).filter(
            Emission.hospital_id == hosp_id,
            Emission.category == "electricity",
            Emission.subcategory == "renewable"
        ).scalar() or 0
        total_elec = db.query(func.sum(Emission.quantity)).filter(
            Emission.hospital_id == hosp_id,
            Emission.category == "electricity"
        ).scalar() or 1  # avoid zero division
        return renewable / total_elec if total_elec else 0

    def calc_waste_segregation(hosp_id):
        incin = db.query(func.sum(Emission.quantity)).filter(
            Emission.hospital_id == hosp_id,
            Emission.category == "biomedical",
            Emission.subcategory == "incinerated"
        ).scalar() or 0
        total = db.query(func.sum(Emission.quantity)).filter(
            Emission.hospital_id == hosp_id,
            Emission.category == "biomedical"
        ).scalar() or 1
        return incin / total if total else 0

    # Your hospital metrics
    your = dict(
        epi=calc_epi(hospital_id, beds),
        emissions_per_bed=calc_emission_per_bed(hospital_id, beds),
        waste_per_bed=calc_waste_per_bed(hospital_id, beds),
        renewable_share=calc_renewable_share(hospital_id),
        waste_segregation=calc_waste_segregation(hospital_id),
    )

    # Peer metrics as list of dicts
    peer_metrics = []
    for pid in peer_ids:
        p_beds = db.query(Hospital.beds).filter(Hospital.id == pid).scalar() or 1
        peer_metrics.append(dict(
            epi=calc_epi(pid, p_beds),
            emissions_per_bed=calc_emission_per_bed(pid, p_beds),
            waste_per_bed=calc_waste_per_bed(pid, p_beds),
            renewable_share=calc_renewable_share(pid),
            waste_segregation=calc_waste_segregation(pid),
        ))

    # Helper for stats
    def stats(metric):
        values = [pm[metric] for pm in peer_metrics]
        if not values: return dict(avg=None, min=None, max=None, p50=None, ranking=None)
        values_sorted = sorted(values)
        n = len(values_sorted)
        # Your hospital value
        y_val = your[metric]
        # Ranking (1 is best if lower is better, reverse for higher better metrics)
        better = sum(1 for v in values if v < y_val) + 1
        # Median (p50)
        if n % 2 == 0:
            p50 = 0.5 * (values_sorted[n // 2 - 1] + values_sorted[n // 2])
        else:
            p50 = values_sorted[n // 2]
        return dict(
            avg=sum(values) / n,
            min=min(values),
            max=max(values),
            p50=p50,
            ranking=better,
            count=n+1
        )

    return {
        "your_metrics": your,
        "epi_benchmark": {**stats("epi"), "your_value": your["epi"]},
        "emissions_per_bed_benchmark": {**stats("emissions_per_bed"), "your_value": your["emissions_per_bed"]},
        "waste_per_bed_benchmark": {**stats("waste_per_bed"), "your_value": your["waste_per_bed"]},
        "renewable_share_benchmark": {**stats("renewable_share"), "your_value": your["renewable_share"]},
        "waste_segregation_benchmark": {**stats("waste_segregation"), "your_value": your["waste_segregation"]},
    }
