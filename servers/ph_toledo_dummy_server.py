from flask import Flask, Response, jsonify
import random

app = Flask(__name__)

# --- API ENDPOINTS ---

@app.route("/read_ph", methods=["GET"])
def read_ph():
    latest_reading = {'pH':round(random.uniform(0, 12), 2),
                      'temperature_C':round(random.uniform(12, 21), 1)}
    if latest_reading is None:
        return jsonify({"pH": "[Warning] No data available yet"}), 503
    return jsonify(latest_reading), 200
    
@app.route("/status", methods=["GET"])
def status():
    latest_reading = None
    if latest_reading is None:
        return jsonify({"status": "waiting_for_device(DEBUG)"}), 200
    return jsonify({"status": "ok"}), 200

# 🏁 Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5013)