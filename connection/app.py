from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
import pyodbc
from auto_update import update_weather_data

app = Flask(__name__)
CORS(app)

# establish connection
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost\\DOKUSSERVER;"
                      "Database=Lernperiode12;"
                      "Trusted_Connection=yes;")

cursor = cnxn.cursor()

@app.route("/weather-measurement")
def weather_measurent():
    cursor.execute("""
        SELECT
            timestamp,
            temperature,
            humidity,
            windspeed,
            precipitation
        FROM WeatherMeasurement
        WHERE timestamp >= DATEADD(HOUR, -48, GETDATE())
          AND temperature IS NOT NULL
          AND humidity IS NOT NULL
          AND windspeed IS NOT NULL
          AND precipitation IS NOT NULL
        ORDER BY timestamp ASC
""")
    
    rows = cursor.fetchall()

    data = [
        {
            "timestamp": row.timestamp.isoformat(),
            "temperature": float(row.temperature),
            "humidity":float(row.humidity),
            "windspeed":float(row.windspeed),
            "precipitation":float(row.precipitation)
        }
        for row in rows
    ]
    
    return jsonify(data)

@app.route("/refresh-data", methods=["POST"])
def refresh_data():
    try:
        update_weather_data()
        return jsonify({"success": True, "message": "Data updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)