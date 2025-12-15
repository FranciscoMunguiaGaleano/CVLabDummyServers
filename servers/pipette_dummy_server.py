from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send_gcode', methods=['POST'])
def send_gcode():
    data = request.get_json()
    if not data or 'gcode' not in data:
        return jsonify({"error": "Missing 'gcode' in request"}), 400

    response = "[DEBUG] Gcode sent."
    return jsonify({"sent": data['gcode'], "response": response})


@app.route('/unlock', methods=['POST'])
def unlock():
    response = "[DEBUG] Unlocked"
    return jsonify({"sent": "$X", "response": response})


@app.route('/home', methods=['POST'])
def home():
    response = "[DEBUG] Home coomand sent."
    return jsonify({"sent": "$H", "response": response})


@app.route('/settings', methods=['GET'])
def settings():
    response = "[DEBUG] Settings"
    return jsonify({"sent": "$$", "response": response})


@app.route('/status', methods=['GET'])
def status():
    response = "[DEBUG] Status"
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