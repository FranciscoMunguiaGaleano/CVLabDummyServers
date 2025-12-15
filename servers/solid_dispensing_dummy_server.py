from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/status", methods=["GET"])
def status():
    connected = "[DEBUG] Dummy solid dispenser connected."
    return jsonify({"connected": connected})

@app.route("/dispense", methods=["POST"])
def dispense():
    """
    Dispense a sample.
    Expects JSON:
    {
        "sample_id": "Sample1",
        "mass": 50.0,
        "tolerance": 1.0,          # optional
        "algorithm": "standard",    # optional, "standard" or "advanced"
        "tapper_intensity": 50,     # optional
        "tapper_duration": 3        # optional
    }
    """
    return jsonify({"success": True, "message": "[DEBUG] Dummy solid dispensing complete."})

@app.route("/open_front_door", methods=["POST"])
def open_front_door():
    return jsonify({"success": True, "message": "[DEBUG] Door open"})

@app.route("/close_front_door", methods=["POST"])
def close_front_door():
    return jsonify({"success": True, "message": "[DEBUG] Door closed"})

@app.route("/open_side_door", methods=["POST"])
def open_side_door():
    return jsonify({"success": True, "message": "[DEBUG] Side door open"})

@app.route("/close_side_door", methods=["POST"])
def close_side_door():
    return jsonify({"success": True, "message": "[DEBUG] Side door closed"})

@app.route("/unlock_dosing_head", methods=["POST"])
def unlock_dosing_head():
    return jsonify({"success": True, "message": "[DEBUG] Dosing head unlocked"})

@app.route("/lock_dosing_head", methods=["POST"])
def lock_dosing_head():
    return jsonify({"success": True, "message": "[DEBUG] Dosing head locked"})

@app.route("/get_sample_data", methods=["GET"])
def get_sample_data():
    return jsonify({"success": True, "message": "[DEBUG] Sample data"})

@app.route("/tare_balance", methods=["POST"])
def tare_balance():
    return jsonify({"success": True, "message": "[DEBUG] Taring balance"})

@app.route("/set_target_mass", methods=["POST"])
def set_target_mass():
    return jsonify({"success": True, "message": "[DEBUG] Target mass set"})
@app.route('/')
def index():
    return "✅ Quantos Dummy Flask server Ready"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5003,
        debug=True,
        use_reloader=False)