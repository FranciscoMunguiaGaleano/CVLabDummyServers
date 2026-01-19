from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def control():
    cmd = request.data.decode().strip()
    
    if cmd.lower() == "home":
        return "[DEBUG] Top carousel System homed.\n"
    
    elif cmd.startswith("go "):
        angle = cmd.split()[1]
        # Simulate movement
        return f"[DEBUG] Top carousel Moved to {angle} degrees.\n"

    return "[DEBUG] Dummy Top carousel running.\n"

if __name__ == '__main__':
    # Listen on all interfaces like the Arduino
    app.run(host='0.0.0.0', port=5006)