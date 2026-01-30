from flask import Flask, request, jsonify
import time

class PipetteBotState:
    def __init__(self):
        self.X_axis = 0.0
        self.Y_axis = 0.0
        self.Z_axis = 0.0
        self.GRIPPER = 0


state = PipetteBotState()

app = Flask(__name__)

@app.route('/send_gcode', methods=['POST'])
def send_gcode():
    data = request.get_json()
    if not data or 'gcode' not in data:
        return jsonify({"error": "Missing 'gcode' in request"}), 400

    gcode = data['gcode'].replace(" ", "")
    state.X_axis = float(gcode.split("X")[1].split("Y")[0])
    state.Y_axis = float(gcode.split("Y")[1].split("Z")[0])
    state.Z_axis = float(gcode.split("Z")[1])
    response = "[DEBUG] Gcode sent.";time.sleep(1)
    print(gcode)
    return jsonify({"sent": data['gcode'], "response": response})

@app.route('/unlock', methods=['POST'])
def unlock():
    response = "[DEBUG] Unlocked"
    return jsonify({"sent": "$X", "response": response})


@app.route('/home', methods=['POST'])
def home():
    response = "[DEBUG] Home coomand sent.";time.sleep(4)
    state.X_axis = 0.0
    state.Y_axis = 0.0 
    state.Z_axis = 0.0
    return jsonify({"sent": "$H", "message": response})



@app.route('/settings', methods=['GET'])
def settings():
    response = "[DEBUG] Settings"
    return jsonify({"sent": "$$", "response": response})


@app.route('/status', methods=['GET'])
def status():
    response = f"[DEBUG] X{state.X_axis}Y{state.Y_axis}Z{state.Z_axis}GRIPPER{state.GRIPPER}"
    return jsonify({"sent": "?", "response": response})


@app.route('/position', methods=['GET'])
def position():
    """Return parsed GRBL state and XYZ position"""
    response = "[DEBUG] Position"
    return jsonify({"sent": "position", "response": response})


@app.route('/sleep', methods=['POST'])
def sleep():
    """Put GRBL into low-power sleep mode"""
    response = "[DEBUG] Sleep"
    return jsonify({"sent": "$SLP", "response": response})

@app.route('/reset', methods=['POST'])
def reset():
    """Soft reset GRBL (Ctrl-X)"""
    try:
        return jsonify({"sent": "Ctrl-X", "response": "GRBL reset"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/wait_until_idle', methods=['GET'])
def wait_until_idle():
    """Poll GRBL until it is truly idle or timeout"""
    return jsonify({"status": "Idle", "position": "123"})

@app.route('/jog', methods=['POST'])
def jog():
    """
    Jog mode: move incrementally or to absolute positions
    Example JSON:
      { "x": 10, "y": 0, "z": 0, "f": 500, "relative": true }
    """
    return jsonify({"sent": "job", "response": "[DEBUG] jogged"})

@app.route('/')
def index():
    return "✅ Pipette Dummy Flask server Ready"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)