# 🌡️Weather Forecasting Application [Click here](https://weather-app-1058693665617.europe-west1.run.app/)
### Author: Virendrasinh Chavda

<p align="justify">
This repository contains the code for a weather forecasting application that predicts various meteorological parameters using advanced machine learning models. Built on a robust tech stack involving <strong>Dash</strong>, <strong>FastAPI</strong>, <strong>Google Cloud BigQuery</strong>, and <strong>Open-Meteo APIs</strong>, the application provides precise and real-time weather forecasts for different cities. This repository includes all necessary backend logic, data ingestion pipelines, and trained models for seamless operation.
</p>

![HomePage](weather.png)

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Detailed Implementation](#detailed-implementation)
5. [Results](#results)
6. [Setup and Installation](#setup-and-installation)
7. [Usage](#usage)
8. [Future Enhancements](#future-enhancements)
9. [Contributing](#contributing)
10. [License](#license)

---

## Overview
<p align="justify">
The Weather Forecasting Application leverages a combination of historical and real-time weather data to predict conditions like temperature, precipitation, cloud cover, wind speed, and snowfall. The system supports multiple cities and integrates <strong>BigQuery</strong> for efficient data storage and query processing. Predictions are made for the next 5 hours, providing users with actionable weather insights. The app uses machine learning models trained on weather patterns, employing scaling techniques to enhance prediction accuracy.
</p>

---

## Features
- <strong>Real-Time Data Fetching</strong>: Retrieves live weather data using Open-Meteo APIs.
- <strong>Multi-Parameter Forecasting</strong>: Predicts temperature, precipitation, cloud cover, wind speed, and snowfall.
- <strong>City-Specific Support</strong>: Covers cities like London, Colchester, and Bristol, with an extensible architecture to include more locations.
- <strong>Automated Data Integration</strong>: Ingests data into Google BigQuery, ensuring efficient data management and processing.
- <strong>Scalable Architecture</strong>: Combines FastAPI for the backend and Dash for a dynamic user interface.
- <strong>Customizable Forecasting Models</strong>: Uses pre-trained models and scaling techniques for reliable predictions.

---

## Technologies Used
- <strong>Dash</strong>: For building the interactive frontend and real-time visualization.
- <strong>FastAPI</strong>: Backend framework to handle API endpoints and machine learning model inference.
- <strong>Google BigQuery</strong>: Primary storage for processed weather data.
- <strong>Open-Meteo API</strong>: To fetch real-time weather data.
- <strong>Python Libraries</strong>:
  - `joblib` for model serialization
  - `pandas` and `numpy` for data processing
  - `scikit-learn` for machine learning and scaling
- <strong>Google Cloud Platform</strong>: For scalable and secure cloud infrastructure.

---

## Detailed Implementation

### Data Ingestion
Automates the ingestion of raw weather data into BigQuery, ensuring schema consistency and periodic updates.

### Backend
Hosts machine learning models for real-time prediction, integrating BigQuery and trained models for accurate forecasting.

### Frontend
Provides an interactive Dash-based UI, displaying current conditions and 5-hour forecasts for various parameters.

### Machine Learning Models
Separate models for each parameter: temperature, precipitation, snowfall, wind speed, and cloud cover. Scaling techniques ensure accurate input/output.

---

## Results

The models were evaluated on historical weather datasets with various performance metrics. Below are the summarized results for each parameter prediction:

| <strong>Parameter<strong>     | <strong>Model Used<strong>      | <strong>MAD Error<strong> |
|--------------------|---------------------|------------|
| <strong>Temperature<strong>   | Gradient Boosting   | 0.08        |
| <strong>Precipitation<strong> | Random Forest       | 0.2       |
| <strong>Cloud Cover<strong>   | CATBOOST     | 1.1       |
| <strong>Wind Speed<strong>    | LGBM         | 0.012  |
| <strong>Snowfall<strong>      | LGBM           | 0.001    |

- <strong>MAE (Mean Absolute Error)</strong>: Lower values indicate higher accuracy.
- <strong>Accuracy</strong>: Represents classification performance for cloud cover conditions.

These results demonstrate the robustness of the models in predicting weather parameters accurately.

---

## Setup and Installation

1. <strong>Clone the Repository</strong>
   ```bash
   git clone https://github.com/VirendraChavda/weather-forecasting.git
   cd weather-forecast
   ```
2. <strong>Install Dependencies</strong>
   ```bash
   pip install -r requirements.txt
   ```
3. <strong>Set Environment Variables Configure Google Cloud credentials and API settings</strong>
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_credentials.json"
   export BACKEND_URL="http://localhost:8080"
   ```
4. <strong>Run Services</strong>
- Backend:
   ```bash
   uvicorn backend:app --host 0.0.0.0 --port 8080
   ```
- Frontend:
   ```bash
   python app.py
   ```
## Usage
<p align="justify">
The application provides real-time weather predictions for selected cities. Users can:
</p>

1. Choose a city from the dropdown menu.
2. View current weather details, including temperature, wind speed, and cloud cover.
3. Access a detailed 5-hour forecast.

The backend dynamically updates predictions using trained models and newly ingested data.

---

## Future Enhancements
- <strong>Extended Forecasts</strong>: Add daily and weekly forecasts.
- <strong>Global Coverage</strong>: Expand support to more cities and regions.
- <strong>Advanced Visualizations</strong>: Incorporate graphs and charts for trend analysis.
- <strong>Ensemble Models</strong>: Combine multiple algorithms for enhanced prediction accuracy.

---

## Contributing
<p align="justify">
We welcome contributions to enhance this project! Please submit issues or pull requests. For significant changes, discuss your ideas in an issue before implementation.
</p>

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
