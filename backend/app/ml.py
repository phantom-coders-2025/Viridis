import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def prepare_emission_timeseries(rows):
    """rows: list of (date, co2e) or SQLAlchemy objects with date, co2e attributes."""
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
    df = df.groupby(pd.Grouper(key="date", freq="ME")).sum().reset_index()
    df = df.sort_values("date")
    df["month_label"] = df["date"].dt.strftime("%b %Y")
    df["month_number"] = range(1, len(df) + 1)
    return df


def train_predict_emissions(df):
    """Linear regression forecasting for next 3 to 6 months."""
    if df is None or len(df) < 2:
        return None, None, None

    X = df[["month_number"]].values
    y = df["co2e"].values

    model = LinearRegression().fit(X, y)

    last_month_num = int(df["month_number"].max())
    last_date = df["date"].max()

    future_offsets = np.arange(last_month_num + 1, last_month_num + 7).reshape(-1, 1)
    predictions = model.predict(future_offsets)
    predictions = [max(0.0, round(float(p), 2)) for p in predictions]

    # Generate month labels for future periods
    future_labels = []
    for i in range(1, 7):
        next_dt = last_date + pd.DateOffset(months=i)
        future_labels.append(next_dt.strftime("%b %Y"))

    return list(future_offsets.flatten()), list(predictions), future_labels
