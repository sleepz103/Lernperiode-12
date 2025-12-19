"""
Auto-update script for weather data
Fetches last 48 hours of weather data and inserts new entries into the database
"""
import pyodbc
import requests
import pandas as pd
from datetime import datetime, timedelta


def get_weather_data(latitude, longitude):
    """Fetch weather data from Open-Meteo API"""
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "precipitation"
        ],
        "past_hours": 48,
        "forecast_days": 0,
        "forecast_hours": 0,
        "timezone": "auto"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch weather data: {e}")
        return None


def update_weather_data():
    """Main function to update weather data in the database"""
    
    # Establish database connection
    print("Connecting to database...")
    cnxn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=localhost\\DOKUSSERVER;"
        "Database=Lernperiode12;"
        "Trusted_Connection=yes;"
    )
    cursor = cnxn.cursor()
    
    try:
        # Get the last saved timestamp from database
        cursor.execute("SELECT MAX(timestamp) FROM WeatherMeasurement")
        last_saved_time = cursor.fetchone()[0]
        
        if last_saved_time is None:
            last_saved_time = datetime.now() - timedelta(hours=48)
            print("No previous data found. Starting from 48 hours ago.")
        else:
            print(f"Last saved time: {last_saved_time}")
        
        # Fetch weather data for Baden, Switzerland
        print("Fetching weather data from Open-Meteo API...")
        baden_lat = 47.475361
        baden_lon = 8.306372
        weather = get_weather_data(baden_lat, baden_lon)
        
        if weather is None:
            print("Failed to fetch weather data. Exiting.")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(weather['hourly'])
        df["time"] = pd.to_datetime(df["time"], utc=True)
        
        # Convert last_saved_time to UTC-aware timestamp
        last_saved_time = pd.to_datetime(last_saved_time, utc=True)
        
        # Filter for new rows only
        df_new = df[df["time"] > last_saved_time]
        
        if df_new.empty:
            print("No new data to insert.")
            return
        
        print(f"Found {len(df_new)} new records to insert.")
        
        # Insert new data
        SQL_STATEMENT = """
        INSERT INTO WeatherMeasurement (
            timestamp,
            temperature,
            humidity,
            windspeed,
            precipitation
        ) VALUES (?, ?, ?, ?, ?)
        """
        
        for _, row in df_new.iterrows():
            cursor.execute(
                SQL_STATEMENT,
                (
                    row["time"],
                    row["temperature_2m"],
                    row["relative_humidity_2m"],
                    row["wind_speed_10m"],
                    row["precipitation"]
                )
            )
        
        cnxn.commit()
        print(f"Successfully inserted {len(df_new)} records.")
        print(f"Latest timestamp: {df_new['time'].max()}")
        
    except Exception as e:
        print(f"Error during update: {e}")
        cnxn.rollback()
    finally:
        cursor.close()
        cnxn.close()
        print("Database connection closed.")


if __name__ == "__main__":
    update_weather_data()
