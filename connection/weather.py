import requests
import json
from datetime import datetime

def get_weather_data(latitude, longitude):
    # Base URL for the Open-Meteo API
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the API request
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "timezone": "auto"
    }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Extract current weather data
        current = data["current"]
        
        # Format and print the weather information
        print("\nCurrent Weather Information:")
        print(f"Temperature: {current['temperature_2m']}°C")
        print(f"Humidity: {current['relative_humidity_2m']}%")
        print(f"Precipitation: {current['precipitation']} mm")
        print(f"Wind Speed: {current['wind_speed_10m']} km/h")
        print(f"Last Updated: {current['time']}")
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

if __name__ == "__main__":
    # Example coordinates for Zurich, Switzerland
    zurich_lat = 47.3769
    zurich_lon = 8.5417
    
    print("Fetching weather data for Zurich...")
    weather_data = get_weather_data(zurich_lat, zurich_lon)
    
    if weather_data:
        # If you want to see the raw JSON data
        print("\nRaw weather data:")
        print(json.dumps(weather_data, indent=2))