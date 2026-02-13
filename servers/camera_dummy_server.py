from flask import Flask, Response, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Dummy Camera Flask server running — use /capture to get an image"

@app.route('/capture', methods=['GET'])
def capture():
    """Return a randomly generated 640x480 JPEG image"""

    # Create random image (480 height, 640 width, 3 color channels)
    random_image = np.random.randint(
        0, 256,
        (480, 640, 3),
        dtype=np.uint8
    )

    # Encode image as JPEG
    success, buffer = cv2.imencode('.jpg', random_image)

    if not success:
        return jsonify({"success": False, "message": "Image encoding failed"}), 500

    return Response(
        buffer.tobytes(),
        mimetype='image/png',
        headers={"Content-Disposition": "inline; filename=image.png"}
    )

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"success": True, "message": "[DEBUG] Dummy camera ready"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)
