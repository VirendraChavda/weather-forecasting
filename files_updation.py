import requests
import pandas as pd
import numpy as np
from joblib import load
from datetime import datetime, timedelta
import joblib
import pytz
import os

import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from google.cloud import bigquery
from google.auth import default
from flask import Flask, jsonify

app = Flask(__name__)

cluster_model = joblib.load('Models/cluster.joblib')
cluster_scaler = joblib.load('Scalers/cluster_scaler.joblib')
x_scaler_cloud = joblib.load('Scalers/x_scaler_cloud.joblib')
y_scaler_cloud = joblib.load('Scalers/y_scaler_cloud.joblib')

# import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "bigquery-key.json"
# Use default credentials from the environment
credentials, project_id = default()

# Initialize BigQuery Client
bq_client = bigquery.Client(credentials=credentials, project=project_id)
#bq_client = bigquery.Client()

# Define BigQuery table references
PROJECT_ID = "project-id" #replace project id with your gcp project id
DATASET_ID = "weather_data"
TABLES = {
    "colchester": f"{PROJECT_ID}.{DATASET_ID}.colchester",
    "london": f"{PROJECT_ID}.{DATASET_ID}.london",
    "bristol": f"{PROJECT_ID}.{DATASET_ID}.bristol",
}

# Function to upload data to BigQuery
def update_bigquery_table(dataframe, table_name):
    try:
        job = bq_client.load_table_from_dataframe(dataframe, table_name)
        job.result()  # Wait for the job to complete
        print(f"Inserted {len(dataframe)} rows into {table_name}.")
    except Exception as e:
        print(f"Failed to insert data into {table_name}: {e}")

def data_extraction(responses, table_name):
    response = responses[0]
    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_is_day = current.Variables(3).Value()
    current_precipitation = current.Variables(4).Value()
    current_rain = current.Variables(5).Value()
    current_showers = current.Variables(6).Value()
    current_snowfall = current.Variables(7).Value()
    current_weather_code = current.Variables(8).Value()
    current_cloud_cover = current.Variables(9).Value()
    current_pressure_msl = current.Variables(10).Value()
    current_surface_pressure = current.Variables(11).Value()
    current_wind_speed_10m = current.Variables(12).Value()
    current_wind_direction_10m = current.Variables(13).Value()
    current_wind_gusts_10m = current.Variables(14).Value()
    
    tt = current.Time()
    # Convert Unix timestamp to datetime object
    local_time = datetime.fromtimestamp(tt)
    # Convert to UTC/GMT timezone
    gmt_timezone = pytz.timezone("UTC")
    gmt_time = local_time.astimezone(gmt_timezone)
    # Format the datetime in the required format
    formatted_time = gmt_time.strftime("%Y-%m-%d %H:%M:%S%z")
    
    new_dic = {
        "date": [formatted_time],
        "temperature_2m": [current_temperature_2m],
        "relative_humidity_2m": [current_relative_humidity_2m],
        'apparent_temperature': [current_apparent_temperature],
        'precipitation': [current_precipitation],
        'rain': [current_rain],
        'showers': [current_showers],
        'snowfall': [current_snowfall],
        'pressure_msl': [current_pressure_msl],
        'surface_pressure': [current_surface_pressure],
        'cloud_cover': [current_cloud_cover],
        'wind_speed_10m': [current_wind_speed_10m],
        'wind_direction_10m': [current_wind_direction_10m],
        'wind_gusts_10m': [current_wind_gusts_10m],
        'is_day': [current_is_day]
    }
    
    new_df = pd.DataFrame(new_dic)
    
    # Ensure the 'date' column is in datetime format
    new_df['date'] = pd.to_datetime(new_df['date'])
    new_df['year'] = new_df['date'].dt.year
    new_df['month'] = new_df['date'].dt.month
    new_df['day'] = new_df['date'].dt.day
    new_df['hour'] = new_df['date'].dt.hour
    # Remove the time component from the 'date' column, keeping only the date
    new_df['date'] = new_df['date'].dt.date
    
    cluster_df = new_df[['temperature_2m', 'precipitation', 'rain', 'showers']]
    scaled_cluster_df = cluster_scaler.transform(cluster_df)
    
    # generate the cluster
    cluster_labels = cluster_model.predict(scaled_cluster_df)

    # Add cluster labels to the original dataset
    new_df['cluster'] = cluster_labels
    new_df['date'] = pd.to_datetime(new_df['date'], format='%d-%m-%Y', errors='coerce').dt.date
    new_df['is_day'] = new_df['is_day'].astype(bool)  # Convert 'is_day' to boolean
    new_df['year'] = new_df['year'].astype(int)  # Ensure 'year' is an integer
    new_df['month'] = new_df['month'].astype(int)  # Ensure 'month' is an integer
    new_df['day'] = new_df['day'].astype(int)  # Ensure 'day' is an integer
    new_df['hour'] = new_df['hour'].astype(int)  # Ensure 'hour' is an integer
    new_df['cluster'] = new_df['cluster'].astype(int)  # Ensure 'cluster' is an integer

    update_bigquery_table(new_df, table_name)

# Define your cache session and retry session
cache_session = requests_cache.CachedSession('.cache', expire_after=600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://api.open-meteo.com/v1/forecast"

# Function to fetch data
def fetch_weather_colchester():
    colchester_params = {
        "latitude": 51.8959,
        "longitude": 0.8919,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain",
            "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
            "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"
        ]
    }
    try:
        colchester_response = openmeteo.weather_api(url, params=colchester_params)
        data_extraction(colchester_response, TABLES["colchester"])
    except Exception as e:
        print(f"Error fetching Colchester weather data: {e}")
        
# Function to fetch data
def fetch_weather_london():
    london_params = {
        "latitude": 51.5072,
        "longitude": 0.1276,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain",
            "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
            "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"
        ]
    }
    try:
        london_response = openmeteo.weather_api(url, params=london_params)
        data_extraction(london_response, TABLES["london"])
    except Exception as e:
        print(f"Error fetching London weather data: {e}")
        
# Function to fetch data
def fetch_weather_bristol():
    bristol_params = {
        "latitude": 51.4545,
        "longitude": 2.5879,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain",
            "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
            "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"
        ]
    }
    try:
        bristol_response = openmeteo.weather_api(url, params=bristol_params)
        data_extraction(bristol_response, TABLES["bristol"])
    except Exception as e:
        print(f"Error fetching Bristol weather data: {e}")


@app.route("/")
def main():
    fetch_weather_colchester()
    fetch_weather_london()
    fetch_weather_bristol()
    return jsonify({"message": "Weather data updated successfully"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use the PORT environment variable or default to 8080
    app.run(host="0.0.0.0", port=port)


