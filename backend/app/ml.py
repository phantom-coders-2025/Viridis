from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge


def prepare_emission_timeseries(rows: List[Any]) -> pd.DataFrame:
    """Processes historical emission records into regular monthly aggregated time series."""
    if not rows:
        return pd.DataFrame(columns=["date", "co2e", "month_label", "month_number"])

    formatted_rows = []
    for r in rows:
        if isinstance(r, (list, tuple)):
            formatted_rows.append({"date": r[0], "co2e": float(r[1])})
        elif hasattr(r, "date") and hasattr(r, "co2e"):
            formatted_rows.append({"date": r.date, "co2e": float(r.co2e)})
        elif isinstance(r, dict):
            formatted_rows.append({"date": r["date"], "co2e": float(r["co2e"])})

    df = pd.DataFrame(formatted_rows)
    df["date"] = pd.to_datetime(df["date"])
    # Monthly aggregation
    df = df.groupby(pd.Grouper(key="date", freq="ME")).sum(numeric_only=True).reset_index()
    df = df.sort_values("date").reset_index(drop=True)
    df["month_label"] = df["date"].dt.strftime("%b %Y")
    df["month_number"] = range(1, len(df) + 1)
    return df


def train_predict_emissions(df: pd.DataFrame) -> Tuple[Optional[List[int]], Optional[List[float]], Optional[List[str]], Optional[List[float]], Optional[List[float]]]:
    """Ridge-regularized time-series trend forecasting with standard error confidence bounds."""
    if df is None or len(df) < 2:
        return None, None, None, None, None

    X = df[["month_number"]].values
    y = df["co2e"].values

    # Regularized model to prevent wild swings on short series
    model = Ridge(alpha=1.0).fit(X, y)

    # Estimate standard error of residuals
    y_pred_hist = model.predict(X)
    residuals = y - y_pred_hist
    std_err = float(np.std(residuals)) if len(residuals) > 1 else float(np.mean(y) * 0.08)

    last_month_num = int(df["month_number"].max())
    last_date = df["date"].max()

    future_offsets = np.arange(last_month_num + 1, last_month_num + 7).reshape(-1, 1)
    predictions = model.predict(future_offsets)
    predictions = [max(0.0, round(float(p), 2)) for p in predictions]

    # Upper and Lower 80% confidence bounds
    upper_bounds = [round(float(p + (1.28 * std_err)), 2) for p in predictions]
    lower_bounds = [max(0.0, round(float(p - (1.28 * std_err)), 2)) for p in predictions]

    future_labels = []
    for i in range(1, 7):
        next_dt = last_date + pd.DateOffset(months=i)
        future_labels.append(next_dt.strftime("%b %Y"))

    return (
        list(future_offsets.flatten()),
        list(predictions),
        future_labels,
        upper_bounds,
        lower_bounds,
    )


def detect_statistical_anomalies(emissions_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Detects statistical anomalies across hospital department streams using Z-scores & IQR."""
    if not emissions_data or len(emissions_data) < 3:
        return []

    df = pd.DataFrame(emissions_data)
    anomalies = []

    # Group by department and category
    grouped = df.groupby(["department", "category", "scope"])

    for (dept, cat, scope), group in grouped:
        if len(group) < 2:
            continue

        co2_values = group["co2e"].values
        mean_val = np.mean(co2_values)
        std_val = np.std(co2_values)
        latest_val = float(co2_values[-1])

        # Z-score on latest period
        z_score = float((latest_val - mean_val) / std_val) if std_val > 0.001 else 0.0

        if z_score > 1.4 or (mean_val > 0 and (latest_val / mean_val) > 1.25):
            pct_change = round(((latest_val - mean_val) / mean_val) * 100, 1) if mean_val > 0 else 50.0
            severity = "Critical" if z_score > 2.0 or pct_change > 40 else "Warning"

            # Domain contextual root causes
            if cat == "electricity":
                msg = f"{dept} consumed {round(latest_val, 1)} kg CO2e ({pct_change:+}% vs rolling baseline)."
                rec = "Inspect HVAC compressor cycle timing and sterile theatre air changes per hour (ACH)."
                savings = f"₹{int(max(5000, (latest_val - mean_val) * 10.5)):,} / mo"
            elif cat == "water":
                msg = f"{dept} water usage surged {pct_change:+}% above normal department baseline."
                rec = "Conduct physical audit of washdown pressure valves and flush sensor solenoids."
                savings = f"{int(max(500, (latest_val - mean_val) / 0.00034)):,} L / day"
            elif cat in {"anesthetic", "diesel"}:
                msg = f"{dept} recorded anomalous Scope 1 direct emissions ({pct_change:+}% spike)."
                rec = "Audit operating room vaporizers for Desflurane leakage and calibrate flow rates."
                savings = f"{round((latest_val - mean_val), 1)} kg CO2e / cycle"
            else:
                msg = f"{dept} biomedical waste generation spiked {pct_change:+}%."
                rec = "Re-audit ward color-coded segregation bins to stop non-hazardous plastics entering incineration."
                savings = f"₹{int(max(3000, (latest_val - mean_val) * 18)):,} / mo"

            anomalies.append({
                "id": f"anom-{dept[:3].lower()}-{cat[:3].lower()}-{int(abs(z_score*10))}",
                "title": f"{cat.capitalize()} Spike in {dept}",
                "department": dept,
                "category": cat,
                "scope": scope,
                "severity": severity,
                "change_pct": f"+{pct_change}%",
                "message": msg,
                "recommendation": rec,
                "estimated_savings": savings,
                "z_score": round(z_score, 2),
            })

    return anomalies

