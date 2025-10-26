import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

def prepare_emission_timeseries(rows):
    # rows: list of (date, co2e) tuples
    # Convert to DataFrame, fill missing months with 0
    df = pd.DataFrame(rows, columns=["date", "co2e"])
    df['date'] = pd.to_datetime(df['date'])
    df = df.groupby(pd.Grouper(key='date', freq='M')).sum().reset_index()
    df = df.sort_values('date')
    df['month_number'] = range(1, len(df)+1)
    return df

def train_predict_emissions(df):
    # Linear regression over months
    X = df[['month_number']].values
    y = df['co2e'].values
    # Not enough data
    if len(X) < 2:
        return None, None
    model = LinearRegression().fit(X, y)
    # Predict trend for next 6 months
    future_months = np.arange(df['month_number'].max()+1, df['month_number'].max()+7).reshape(-1,1)
    predictions = model.predict(future_months)
    return list(future_months.flatten()), list(predictions)
