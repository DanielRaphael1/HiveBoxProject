from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import os

app = Flask(__name__)

VERSION = "v0.0.1"  # or load from file

# Define 3 boxes with their corresponding temperature sensor IDs
BOXES = [
    {
        "name": "Box A",
        "box_id": os.getenv("BOX1_ID", "5eba5fbad46fb8001b799786"),
        "sensor_id": os.getenv("BOX1_TEMP_ID", "5eba5fbad46fb8001b799789")
    },
    {
        "name": "Box B",
        "box_id": os.getenv("BOX2_ID", "5c21ff8f919bf8001adf2488"),
        "sensor_id": os.getenv("BOX2_TEMP_ID", "5c21ff8f919bf8001adf248d")
    },
    {
        "name": "Box C",
        "box_id": os.getenv("BOX3_ID", " 5ade1acf223bd80019a1011c"),
        "sensor_id": os.getenv("BOX3_TEMP_ID", "5ade1acf223bd80019a1011e")
    }
]

@app.route('/')
def version():
    return {"version": VERSION}

@app.route('/temperature')
def temperature():
    one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z"
    results = []

    for box in BOXES:
        url = f"https://api.opensensemap.org/boxes/{box['box_id']}/data/{box['sensor_id']}?from-date={one_hour_ago}"

        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            results.append({
                "box": box["name"],
                "sensor_id": box["sensor_id"],
                "measurements_last_hour": data,
                "count": len(data)
            })
        except Exception as e:
            results.append({
                "box": box["name"],
                "error": str(e)
            })
            
    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

