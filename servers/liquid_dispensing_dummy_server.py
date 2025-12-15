from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Configuration ---
PUMP_PORT = "/dev/dispenser_of_liquids"        
SWITCH_ADDRESS = "0"
SYRINGE_SIZE = "12.5mL"
VALVE_TYPE = "6PORT_DISTR"
WASTE_PORT = "O4"
WATER_PORT = "I2"

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"success": True, "message": "[DEBUG] Dummy Liquid Status"})
        
@app.route("/get_valve_pos", methods=["GET"])
def get_valve_pos():
    return jsonify({"success": True, "message": "[DEBUG] Dummy Liquid Valve position"})


@app.route("/dispense", methods=["POST"])
def dispense():
    return jsonify({"success": True, "message": "[DEBUG] Dummy Liquid Dispensing"})

@app.route("/move_home", methods=["POST"])
def move_home():
	return jsonify({"success": True, "message": "[DEBUG] Dummy Liquid Home"})

@app.route("/set_waste_port", methods=["POST"])
def set_waste_port():
	return jsonify({"success": True, "message": "[DEBUG] Dummy liquid set waste port"})

@app.route('/')
def index():
    return "✅ Liquid dispenser Dummy Flask server Ready"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5004,
        debug=True,
        use_reloader=False
    )