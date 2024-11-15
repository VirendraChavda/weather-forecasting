import dash
from dash import dcc, html, Input, Output
import requests
from datetime import datetime, timedelta
import pytz
import os

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Weather Forecast"
server = app.server  # This is needed for gunicorn

# Backend API URL
BACKEND_URL = "your_app_url_here"

# Helper function to fetch weather data from the backend
def fetch_weather_data(city):
    try:
        response = requests.get(f"{BACKEND_URL}/weather/{city}")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching data: {str(e)}"}

# Helper function to determine appropriate icon based on condition and day/night status
def get_weather_icon(condition, is_day):
    if condition == "clear":
        return "clear-day.png" if is_day == True else "clear-night.png"
    elif condition == "cloudy":
        return "cloudy-day.png" if is_day == True else "cloudy-night.png"
    elif condition == "rain and clear":
        return "rain-day.png" if is_day == True else "rain-night.png"
    elif condition == "rain and cloudy":
        return "rain.png"
    elif condition == "snow and clear":
        return "snow-day.png" if is_day == True else "snow-night.png"
    elif condition == "snow and cloudy":
        return "snowy.png"
    return "default.png"

# Helper function to get current time
def get_current_time():
    tz = pytz.timezone("GMT")
    return datetime.now(tz)

# App layout
app.layout = html.Div(
    children=[
        # Header with title, current time, and dropdown
        html.Div(
            children=[
                html.Div("Weather Forecast", className="header-title"),
                html.Div(id="current-time-display", className="current-time"),
                dcc.Dropdown(
                    id="city-dropdown",
                    options=[
                        {"label": "Colchester", "value": "Colchester"},
                        {"label": "London", "value": "London"},
                        {"label": "Bristol", "value": "Bristol"},
                    ],
                    value="Colchester",
                    placeholder="Select a city...",
                    className="dropdown",
                ),
            ],
            className="header",
        ),
        # Weather display content in a responsive container
        html.Div(id="weather-display", className="weather-section"),

        # Footer Section
        html.Div(
            children=[
                html.Div(
                    "Developed by Virendrasinh Chavda using Machine Learning and Dash. © 2024 All rights reserved.",
                    className="footer-content",
                ),
            ],
            className="footer",
        ),
    ],
    className="app-container",
)

# Callback to update current time display
@app.callback(
    Output("current-time-display", "children"),
    [Input("city-dropdown", "value")]
)
def update_current_time(city):
    current_time = get_current_time()
    return f"{current_time.strftime('%I:%M %p %Z')}"

# Callback to update weather display
@app.callback(
    Output("weather-display", "children"),
    [Input("city-dropdown", "value")]
)
def update_weather_display(city):
    # Fetch weather data
    weather_data = fetch_weather_data(city)
    if "error" in weather_data:
        return html.Div(weather_data["error"], className="error-message")

    current_weather = weather_data["current"]
    forecast = weather_data["forecast"]

    # Add `is_day` to each forecast element, assuming the same `is_day` as the current weather
    for hour in forecast:
        hour['is_day'] = current_weather['is_day']

    # Determine text color class based on day or night
    text_class = "day-text" if current_weather['is_day'] else "night-text"

    # Get the current time and calculate the next 5 hours
    current_time = get_current_time()
    forecast_times = [(current_time + timedelta(hours=i + 1)).strftime('%I:%M %p %Z') for i in range(5)]

    # Determine the correct icon for current weather
    current_weather_icon = get_weather_icon(current_weather['conditions'], current_weather['is_day'])

    # Current weather details
    current_details = html.Div(
        children=[
            html.Div(
                children=[
                    html.Img(
                        src=f"/assets/{current_weather_icon}",
                        className="current-weather-icon",
                    ),
                    html.Div(
                        children=[
                            html.H2(f"{city}", className=f"weather-title {text_class}"),
                            html.P(f"Temperature: {current_weather['temperature']}°C", className=text_class),
                            html.P(f"Feels Like: {current_weather['feels_like']}°C", className=text_class),
                            html.P(f"Wind Speed: {current_weather['windspeed']} km/h", className=text_class),
                            html.P(f"Precipitation: {current_weather['precipitation']} mm", className=text_class),
                            html.P(f"Humidity: {current_weather['humidity']} %", className=text_class),
                            html.P(f"Pressure: {current_weather['pressure']} mb", className=text_class),
                        ],
                        className="current-weather-details",
                    ),
                ],
                className="current-weather-card",
            ),
        ]
    )

    # Forecast details
    forecast_details = html.Div(
        children=[
            html.H5("Next 5 Hours Forecast", className=f"forecast-title {text_class}"),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.P(f"{forecast_times[i]}", className=f"forecast-hour {text_class}"),
                            html.Img(
                                src=f"/assets/{get_weather_icon(hour['conditions'], hour['is_day'])}",
                                className="forecast-icon",
                            ),
                            html.P(children=[html.Img(src="/assets/thermometer.png", className="thermometer-icon"), f" {hour['temperature']}°C"], className=f"forecast-temp {text_class}"),
                            html.P(children=[html.Img(src="/assets/wind.png", className="wind-icon"), f" {hour['wind']} km/h"], className=f"forecast-wind {text_class}"),
                            html.P(children=[html.Img(src="/assets/precipitation.png", className="precipitation-icon"), f" {hour['precipitation']} %"], className=f"forecast-precipitation {text_class}"),
                        ],
                        className="forecast-card",
                    )
                    for i, hour in enumerate(forecast[:5])
                ],
                className="forecast-container",
            ),
        ],
        className="forecast-section",
    )

    return html.Div(
        children=[current_details, forecast_details],
        className=f"app-container {'day-background' if current_weather['is_day'] else 'night-background'}",
    )

# # Run using gunicorn server on specified port
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8050))
#     app.run_server(host="0.0.0.0", port=port, debug=True)


#Run using gunicorn server on specified port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run_server(host="0.0.0.0", port=port, debug=True)