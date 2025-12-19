from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv
import pyodbc

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

if __name__ == "__main__":
    app.run(debug=True)