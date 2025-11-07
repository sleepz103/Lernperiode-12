import random
from datetime import datetime
import json

class EnvironmentalMonitor:
    def __init__(self, sensor_location):
        self.sensor_location = sensor_location
        # Define optimal ranges for the plant
        self.optimal_ranges = {
            "soil_moisture": (40, 60),  # percentage
            "soil_temperature": (18, 24),  # Celsius
            "ambient_temperature": (20, 25),  # Celsius
            "light_level": (800, 1200),  # lux
            "humidity": (45, 65)  # percentage
        }
    
    def get_readings(self):
        current_time = datetime.now().isoformat()
        readings = {
            "timestamp": current_time,
            "soil_moisture": round(random.uniform(30, 70), 2),
            "soil_temperature": round(random.uniform(15, 28), 2),
            "ambient_temperature": round(random.uniform(18, 30), 2),
            "light_level": round(random.uniform(500, 1500), 2),
            "humidity": round(random.uniform(40, 70), 2)
        }
        
        # Add status for each measurement
        status = self._check_conditions(readings)
        readings["status"] = status
        
        return readings
    
    def _check_conditions(self, readings):
        status = {}
        for measure, value in readings.items():
            if measure == "timestamp":
                continue
            optimal_range = self.optimal_ranges.get(measure)
            if optimal_range:
                if value < optimal_range[0]:
                    status[measure] = "Too Low"
                elif value > optimal_range[1]:
                    status[measure] = "Too High"
                else:
                    status[measure] = "Optimal"
        return status

def print_readings(monitor):
    readings = monitor.get_readings()
    
    print("\nEnvironmental Readings for:", monitor.sensor_location)
    print("-" * 50)
    print(f"Time: {readings['timestamp']}")
    print("\nCurrent Conditions:")
    print(f"Soil Moisture: {readings['soil_moisture']}%")
    print(f"Soil Temperature: {readings['soil_temperature']}°C")
    print(f"Ambient Temperature: {readings['ambient_temperature']}°C")
    print(f"Light Level: {readings['light_level']} lux")
    print(f"Humidity: {readings['humidity']}%")
    
    print("\nStatus Report:")
    for measure, status in readings['status'].items():
        print(f"{measure.replace('_', ' ').title()}: {status}")
    
    print("\nOptimal Ranges:")
    for measure, (min_val, max_val) in monitor.optimal_ranges.items():
        print(f"{measure.replace('_', ' ').title()}: {min_val}-{max_val}")

if __name__ == '__main__':
    # Create monitor instance
    monitor = EnvironmentalMonitor("Neverdie Station")
    
    # Display the readings
    print_readings(monitor)
    
    # Show raw data
    print("\nRaw JSON data:")
    print(json.dumps(monitor.get_readings(), indent=2))