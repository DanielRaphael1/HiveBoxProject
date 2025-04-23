from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

VERSION = "v0.0.2"

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
        "box_id": os.getenv("BOX3_ID", "5ade1acf223bd80019a1011c"),
        "sensor_id": os.getenv("BOX3_TEMP_ID", "5ade1acf223bd80019a1011e")
    }
]

@app.route('/version')
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

            temps = [float(d["value"]) for d in data if "value" in d]
            avg_temp = sum(temps) / len(temps) if temps else None

            # Determine status
            if avg_temp is not None:
                if avg_temp < 10:
                    status = "Too Cold"
                elif avg_temp > 37:
                    status = "Too Hot"
                else:
                    status = "Good"
            else:
                status = "No Data"

            results.append({
                "box": box["name"],
                "sensor_id": box["sensor_id"],
                "measurements_last_hour": data,
                "count": len(data),
                "average_temperature": avg_temp,
                "status": status
            })
        except Exception as e:
            results.append({
                "box": box["name"],
                "error": str(e)
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)