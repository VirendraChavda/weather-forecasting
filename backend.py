from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import pandas as pd
import numpy as np
from joblib import load
import joblib
from datetime import datetime

import pandas as pd
from retry_requests import retry
from google.cloud import bigquery
from google.auth import default

# Initialize FastAPI app
app = FastAPI()
# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this to your frontend's URL)
    allow_methods=["*"],
    allow_headers=["*"],
)

# import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bigquery-key.json"
# #Initialize BigQuery Client
# bq_client = bigquery.Client()

# Use default credentials from the environment
credentials, project_id = default()
bq_client = bigquery.Client(credentials=credentials, project=project_id)

# Define BigQuery table references
PROJECT_ID = "gcp_project_id_here"
DATASET_ID = "weather_data"
TABLES = {
    "colchester": f"{PROJECT_ID}.{DATASET_ID}.colchester",
    "london": f"{PROJECT_ID}.{DATASET_ID}.london",
    "bristol": f"{PROJECT_ID}.{DATASET_ID}.bristol",
}

def load_data(table_name):
    query = f"""
    SELECT *
    FROM `{table_name}`
    """
    query_job = bq_client.query(query)
    results = query_job.result()
    table = results.to_arrow()  # Use Arrow for conversion
    data = table.to_pandas()
    data = data.iloc[len(data.index)-5 : ].reset_index(drop = True)
    data["is_day"] = data["is_day"].astype(int)
    return data

# Replace CSV loading with BigQuery data fetching
# colchester_weather = load_data(TABLES['colchester'])
# london_weather = load_data(TABLES['london'])
# bristol_weather = load_data(TABLES['bristol'])


temperature_model = joblib.load('Models/temperature_model.joblib')
rain_model = joblib.load('Models/rain_model.joblib')
cloud_model = joblib.load('Models/cloud_cover_model.joblib')
windspeed_model = joblib.load('Models/wind_model.joblib')
snow_model = joblib.load('Models/snow_model.joblib')
x_scaler_cloud = joblib.load('Scalers/x_scaler_cloud.joblib')
y_scaler_cloud = joblib.load('Scalers/y_scaler_cloud.joblib')
x_scaler_rain = joblib.load('Scalers/x_scaler_rain.joblib')
y_scaler_rain = joblib.load('Scalers/y_scaler_rain.joblib')
x_scaler_snow = joblib.load('Scalers/x_scaler_snow.joblib')
y_scaler_snow = joblib.load('Scalers/y_scaler_snow.joblib')
x_scaler_temperature = joblib.load('Scalers/x_scaler_temperature.joblib')
y_scaler_temperature = joblib.load('Scalers/y_scaler_temperature.joblib')
x_scaler_wind = joblib.load('Scalers/x_scaler_wind.joblib')
y_scaler_wind = joblib.load('Scalers/y_scaler_wind.joblib')

def predict_temp(data):
    data = data[['temperature_2m', 'apparent_temperature', 'showers', 'cloud_cover', 'wind_speed_10m', 'month',
                 'day', 'cluster']]

    lagged_data = data.copy()
    for lag in range(1, 2):  # Create lags
        for col in data.columns:
            lagged_data[f'{col}_lag_{lag}'] = data[col].shift(lag)

    for lag in range(1, 6):
        lagged_data[f'future_temp_{lag}'] = lagged_data['temperature_2m'].shift(-lag)
        
    x = lagged_data.drop(['future_temp_1', 'future_temp_2', 'future_temp_3', 'future_temp_4', 'future_temp_5'], axis = 1)
    x = pd.DataFrame([x.iloc[-1]]).reset_index(drop = True)
    x = x_scaler_temperature.transform(x)
    
    pred = temperature_model.predict(x)
    pred = y_scaler_temperature.inverse_transform(pred)
    
    list_data = pred.tolist()[0]
    list_data = [round(x) for x in list_data]
    return list_data

def predict_rain(data):
    data = data[['precipitation', 'apparent_temperature', 'showers', 'pressure_msl', 'cloud_cover', 'wind_direction_10m',
          'wind_gusts_10m', 'is_day', 'month', 'day', 'cluster']]

    lagged_data = data.copy()
    for lag in range(1, 3):  # Create lags
        for col in data.columns:
            lagged_data[f'{col}_lag_{lag}'] = data[col].shift(lag)

    for lag in range(1, 6):
        lagged_data[f'future_rain_{lag}'] = lagged_data['precipitation'].shift(-lag)
        
    x = lagged_data.drop(['future_rain_1', 'future_rain_2', 'future_rain_3', 'future_rain_4', 'future_rain_5'], axis = 1)
    x = pd.DataFrame([x.iloc[-1]]).reset_index(drop = True)
    x = x_scaler_rain.transform(x)
    
    pred = rain_model.predict(x)
    pred = y_scaler_rain.inverse_transform(pred)
    
    list_data = pred.tolist()[0]
    list_data = [x if x >= 0 else 0 for x in list_data]
    list_data = [round(x, 1) for x in list_data]
    return list_data

def predict_snow(data):
    data = data[['snowfall', 'precipitation']]

    lagged_data = data.copy()
    for lag in range(1, 2):  # Create lags
        for col in data.columns:
            lagged_data[f'{col}_lag_{lag}'] = data[col].shift(lag)

    for lag in range(1, 6):
        lagged_data[f'future_snow_{lag}'] = lagged_data['snowfall'].shift(-lag)
        
    x = lagged_data.drop(['future_snow_1', 'future_snow_2', 'future_snow_3', 'future_snow_4', 'future_snow_5'], axis = 1)
    x = pd.DataFrame([x.iloc[-1]]).reset_index(drop = True)
    x = x_scaler_snow.transform(x)
    
    pred = snow_model.predict(x)
    pred = y_scaler_snow.inverse_transform(pred)
    
    list_data = pred.tolist()[0]
    list_data = [x if x >= 0 else 0 for x in list_data]
    list_data = [round(x, 1) for x in list_data]
    return list_data

def predict_cloud_cover(data):
    data = data[['cloud_cover', 'temperature_2m', 'relative_humidity_2m', 'apparent_temperature', 'precipitation', 'rain',
          'showers', 'snowfall', 'pressure_msl', 'wind_speed_10m', 'wind_direction_10m', 'wind_gusts_10m', 'is_day',
          'month', 'day', 'hour', 'cluster']]

    lagged_data = data.copy()
    for lag in range(1, 2):  # Create lags
        for col in data.columns:
            lagged_data[f'{col}_lag_{lag}'] = data[col].shift(lag)

    for lag in range(1, 6):
        lagged_data[f'future_cloud_{lag}'] = lagged_data['cloud_cover'].shift(-lag)
        
    x = lagged_data.drop(['future_cloud_1', 'future_cloud_2', 'future_cloud_3', 'future_cloud_4', 'future_cloud_5'], axis = 1)
    x = pd.DataFrame([x.iloc[-1]]).reset_index(drop = True)
    x = x_scaler_cloud.transform(x)
    
    pred = cloud_model.predict(x)
    pred = y_scaler_cloud.inverse_transform(pred)
    
    list_data = pred.tolist()[0]
    list_data = [x if x >= 0 else 0 for x in list_data]
    list_data = [round(x) for x in list_data]
    return list_data

def predict_windspeed(data):
    data = data[['wind_speed_10m', 'temperature_2m', 'apparent_temperature', 'precipitation', 'rain', 'showers', 'snowfall',
          'pressure_msl', 'surface_pressure', 'cloud_cover', 'wind_direction_10m', 'wind_gusts_10m', 'is_day', 'month', 'day',
          'hour', 'cluster']]

    lagged_data = data.copy()
    for lag in range(1, 2):  # Create lags
        for col in data.columns:
            lagged_data[f'{col}_lag_{lag}'] = data[col].shift(lag)

    for lag in range(1, 6):
        lagged_data[f'future_windspeed_{lag}'] = lagged_data['wind_speed_10m'].shift(-lag)
        
    x = lagged_data.drop(['future_windspeed_1', 'future_windspeed_2', 'future_windspeed_3', 'future_windspeed_4',
                          'future_windspeed_5'], axis = 1)
    x = pd.DataFrame([x.iloc[-1]]).reset_index(drop = True)
    x = x_scaler_wind.transform(x)
    
    pred = windspeed_model.predict(x)
    pred = y_scaler_wind.inverse_transform(pred)
    
    list_data = pred.tolist()[0]
    list_data = [x if x >= 0 else 0 for x in list_data]
    list_data = [round(x, 1) for x in list_data]
    return list_data

def categorize_weather(row):
    # Extract relevant values
    precipitation = row['precipitation']
    snowfall = row['snowfall']
    cloud_cover = row['cloud_cover']

    # Sunny
    if precipitation == 0 and cloud_cover < 40:
        return 'clear'
    
    # Cloudy
    elif precipitation == 0 and cloud_cover >= 40:
        return 'cloudy'
    
    # Rain and Sunny
    elif precipitation > 0 and cloud_cover < 40:
        return 'rain and clear'
    
    # Rain and Cloudy
    elif precipitation > 0 and cloud_cover >= 40:
        return 'rain and cloudy'
    
    # Snow and Sunny
    elif snowfall > 0 and cloud_cover < 40:
        return 'snow and clear'
    
    # Snow and Cloudy
    elif snowfall > 0 and cloud_cover >= 40:
        return 'snow and cloudy'

def forecast_weather(data):
    tempre_list = predict_temp(data)
    precipitation_list = predict_rain(data)
    snow_list = predict_snow(data)
    cloud_list = predict_cloud_cover(data)
    windspeed_list = predict_windspeed(data)
    
    forecast_df = pd.DataFrame({
        "temperature": tempre_list,
        "precipitation": precipitation_list,
        "snowfall": snow_list,
        "cloud_cover": cloud_list,
        "wind": windspeed_list
    })

    forecast_df['conditions']  = forecast_df.apply(categorize_weather, axis=1)
    
    now_df = pd.DataFrame([data.iloc[-1]]).reset_index(drop = True)
    now_df['conditions']  = now_df.apply(categorize_weather, axis=1)
    
    return {
        "forecast": forecast_df.to_dict(orient="records"),
        "current": {
            "temperature": int(round(now_df.temperature_2m[0])),
            "feels_like": int(round(now_df.apparent_temperature[0])),
            "precipitation": round(now_df.precipitation[0]),
            "snowfall": round(now_df.snowfall[0]),
            "windspeed": round(now_df.wind_speed_10m[0], 1),
            "conditions": now_df.conditions[0],
            "is_day": bool(now_df.is_day[0]),
            "humidity": round(now_df.relative_humidity_2m[0]),
            "pressure": round(now_df.surface_pressure[0], 1)
        },
    }


# Route to get weather data for a city
@app.get("/weather/{city}")
async def get_predicted_data(city: str):
    city = city.lower()
    if city not in TABLES:
        raise HTTPException(status_code=404, detail="City not found")
    
    # Load data dynamically for the city
    data = load_data(TABLES[city])
    forecast = forecast_weather(data)

    return forecast