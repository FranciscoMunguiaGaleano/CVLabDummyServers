from flask import Flask, Response, jsonify
import cv2
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Dummy Camera Flask server running — use /capture to get an image"

@app.route('/capture', methods=['GET'])
def capture():
    """Capture and return latest frame as JPEG"""
    return jsonify({"success": True, "message": "[DEBUG] Dummy image"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"success": True, "message": "[DEBUG] Dummy camwera readt"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)