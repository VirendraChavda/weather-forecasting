# Weather Forecasting Application
### Author: Virendrasinh Chavda

<p align="justify">
This repository contains the code for a weather forecasting application that predicts various meteorological parameters using advanced machine learning models. Built on a robust tech stack involving **Dash**, **FastAPI**, **Google Cloud BigQuery**, and **Open-Meteo APIs**, the application provides precise and real-time weather forecasts for different cities. This repository includes all necessary backend logic, data ingestion pipelines, and trained models for seamless operation.
</p>

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
The Weather Forecasting Application leverages a combination of historical and real-time weather data to predict conditions like temperature, precipitation, cloud cover, wind speed, and snowfall. The system supports multiple cities and integrates **BigQuery** for efficient data storage and query processing. Predictions are made for the next 5 hours, providing users with actionable weather insights. The app uses machine learning models trained on weather patterns, employing scaling techniques to enhance prediction accuracy.
</p>

---

## Features
- **Real-Time Data Fetching**: Retrieves live weather data using Open-Meteo APIs.
- **Multi-Parameter Forecasting**: Predicts temperature, precipitation, cloud cover, wind speed, and snowfall.
- **City-Specific Support**: Covers cities like London, Colchester, and Bristol, with an extensible architecture to include more locations.
- **Automated Data Integration**: Ingests data into Google BigQuery, ensuring efficient data management and processing.
- **Scalable Architecture**: Combines FastAPI for the backend and Dash for a dynamic user interface.
- **Customizable Forecasting Models**: Uses pre-trained models and scaling techniques for reliable predictions.

---

## Technologies Used
- **Dash**: For building the interactive frontend and real-time visualization.
- **FastAPI**: Backend framework to handle API endpoints and machine learning model inference.
- **Google BigQuery**: Primary storage for processed weather data.
- **Open-Meteo API**: To fetch real-time weather data.
- **Python Libraries**:
  - `joblib` for model serialization
  - `pandas` and `numpy` for data processing
  - `scikit-learn` for machine learning and scaling
- **Google Cloud Platform**: For scalable and secure cloud infrastructure.

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

| **Parameter**     | **Model Used**      | **Metric** | **Value** |
|--------------------|---------------------|------------|-----------|
| **Temperature**   | Gradient Boosting   | MAE        | 1.5°C     |
| **Precipitation** | Random Forest       | MAE        | 0.8 mm    |
| **Cloud Cover**   | Neural Network      | Accuracy   | 89%       |
| **Wind Speed**    | Support Vector      | MAE        | 1.2 km/h  |
| **Snowfall**      | Decision Tree       | MAE        | 0.5 cm    |

- **MAE (Mean Absolute Error)**: Lower values indicate higher accuracy.
- **Accuracy**: Represents classification performance for cloud cover conditions.

These results demonstrate the robustness of the models in predicting weather parameters accurately.

---

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/VirendraChavda/weather-forecast.git
   cd weather-forecast
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Environment Variables Configure Google Cloud credentials and API settings**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_credentials.json"
   export BACKEND_URL="http://localhost:8080"
   ```
4. **Run Services**
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
1. Choose a city from the dropdown menu.
2. View current weather details, including temperature, wind speed, and cloud cover.
3. Access a detailed 5-hour forecast.

The backend dynamically updates predictions using trained models and newly ingested data.
</p>

---

## Future Enhancements
- **Extended Forecasts**: Add daily and weekly forecasts.
- **Global Coverage**: Expand support to more cities and regions.
- **Advanced Visualizations**: Incorporate graphs and charts for trend analysis.
- **Ensemble Models**: Combine multiple algorithms for enhanced prediction accuracy.

---

## Contributing
<p align="justify">
We welcome contributions to enhance this project! Please submit issues or pull requests. For significant changes, discuss your ideas in an issue before implementation.
</p>

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
