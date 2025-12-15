from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def control():
    cmd = request.data.decode().strip()
    
    if cmd.lower() == "home":
        return "[DEBUG] Bottom carousel System homed.\n"
    
    elif cmd.startswith("go "):
        angle = cmd.split()[1]
        # Simulate movement
        return f"[DEBUG] Bottom Moved to {angle} degrees.\n"

    return "[DEBUG] Dummy Bottom carouselrunning.\n"

if __name__ == '__main__':
    # Listen on all interfaces like the Arduino
    app.run(host='0.0.0.0', port=5007)