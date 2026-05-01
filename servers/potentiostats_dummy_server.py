import matplotlib
matplotlib.use("Agg")  

from flask import Flask, Response, jsonify
import numpy as np
import matplotlib.pyplot as plt
import io
import time
import random
import csv

app = Flask(__name__)

# -----------------------------------
# CACHE 
# -----------------------------------
LAST_RESULTS = {}

# -----------------------------------
# HELPERS
# -----------------------------------

def generate_cv_data(start, vertex, cycles, points=200):
    x = []
    y = []

    for _ in range(cycles):
        forward = np.linspace(start, vertex, points)
        backward = np.linspace(vertex, start, points)

        for v in forward:
            x.append(v)
            y.append(np.sin(v * 3) + random.uniform(-0.05, 0.05))

        for v in backward:
            x.append(v)
            y.append(np.sin(v * 3) * 0.8 + random.uniform(-0.05, 0.05))

    return x, y


def generate_linear_data(start, end, points=200):
    x = np.linspace(start, end, points)
    y = 0.5 * x + np.random.normal(0, 0.02, points)
    return x, y


def generate_time_series(duration, sampling):
    t = np.arange(0, duration, sampling)
    return t


def to_csv_bytes(x, y, xlabel, ylabel):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([xlabel, ylabel])

    for xi, yi in zip(x, y):
        writer.writerow([xi, yi])

    return output.getvalue().encode("utf-8")


def make_plot(x, y, title, xlabel, ylabel):
    plt.figure()
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf


def error_plot(title):
    plt.figure()
    plt.text(0.5, 0.5, "ERROR", ha="center", va="center")
    plt.title(title)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf


# -----------------------------------
# STATUS
# -----------------------------------

@app.route("/<int:p_id>/status", methods=["GET"])
def status(p_id):
    return jsonify({"status": "ok", "device": p_id})


# -----------------------------------
# CYCLIC VOLTEMMETRY (CSV)
# -----------------------------------

@app.route("/<int:p_id>/cyclic_voltemmetry", methods=["POST"])
def cyclic_voltemmetry(p_id):
    try:
        time.sleep(1.5)  # simulate experiment time

        x, y = generate_cv_data(0, 1, cycles=1)

        csv_bytes = to_csv_bytes(x, y, "Potential", "Current")

        LAST_RESULTS[(p_id, "cv")] = (x, y)

        return Response(csv_bytes, mimetype="text/csv")

    except Exception:
        LAST_RESULTS.pop((p_id, "cv"), None)
        return jsonify({"error": "CV failed"}), 500


# -----------------------------------
# CYCLIC VOLTEMMETRY (PLOT)
# -----------------------------------

@app.route("/<int:p_id>/cyclic_voltemmetry/plot", methods=["GET"])
def cv_plot(p_id):
    key = (p_id, "cv")

    data = LAST_RESULTS.get(key)

    if data is None:
        return Response(error_plot("No CV Data"), mimetype="image/png")

    x, y = data

    img = make_plot(x, y, f"CV P{p_id}", "Potential", "Current")

    LAST_RESULTS.pop(key, None)

    return Response(img, mimetype="image/png")


# -----------------------------------
# LINEAR VOLTEMMETRY
# -----------------------------------

@app.route("/<int:p_id>/linear_voltemmetry", methods=["POST"])
def linear_voltemmetry(p_id):
    try:
        time.sleep(1)

        x, y = generate_linear_data(0, 1)

        csv_bytes = to_csv_bytes(x, y, "Potential", "Current")

        LAST_RESULTS[(p_id, "lv")] = (x, y)

        return Response(csv_bytes, mimetype="text/csv")

    except Exception:
        LAST_RESULTS.pop((p_id, "lv"), None)
        return jsonify({"error": "LV failed"}), 500


@app.route("/<int:p_id>/linear_voltemmetry/plot", methods=["GET"])
def lv_plot(p_id):
    key = (p_id, "lv")

    data = LAST_RESULTS.get(key)

    if data is None:
        return Response(error_plot("No LV Data"), mimetype="image/png")

    x, y = data

    img = make_plot(x, y, f"LV P{p_id}", "Potential", "Current")

    LAST_RESULTS.pop(key, None)

    return Response(img, mimetype="image/png")


# -----------------------------------
# OPEN CIRCUIT
# -----------------------------------

@app.route("/<int:p_id>/open_circuit", methods=["POST"])
def open_circuit(p_id):
    try:
        time.sleep(1)

        t = generate_time_series(10, 0.1)
        v = np.sin(t) * 0.1 + 0.5

        csv_bytes = to_csv_bytes(t, v, "Time", "Potential")

        LAST_RESULTS[(p_id, "oc")] = (t, v)

        return Response(csv_bytes, mimetype="text/csv")

    except Exception:
        LAST_RESULTS.pop((p_id, "oc"), None)
        return jsonify({"error": "OCP failed"}), 500


@app.route("/<int:p_id>/open_circuit/plot", methods=["GET"])
def oc_plot(p_id):
    key = (p_id, "oc")

    data = LAST_RESULTS.get(key)

    if data is None:
        return Response(error_plot("No OCP Data"), mimetype="image/png")

    t, v = data

    img = make_plot(t, v, f"OCP P{p_id}", "Time", "Potential")

    LAST_RESULTS.pop(key, None)

    return Response(img, mimetype="image/png")


# -----------------------------------
# ELECTROLYSIS
# -----------------------------------

@app.route("/<int:p_id>/electrolysis", methods=["POST"])
def electrolysis(p_id):
    try:
        time.sleep(1)

        t = generate_time_series(10, 0.1)
        i = np.exp(-t / 5) + np.random.normal(0, 0.01, len(t))

        csv_bytes = to_csv_bytes(t, i, "Time", "Current")

        LAST_RESULTS[(p_id, "el")] = (t, i)

        return Response(csv_bytes, mimetype="text/csv")

    except Exception:
        LAST_RESULTS.pop((p_id, "el"), None)
        return jsonify({"error": "Electrolysis failed"}), 500


@app.route("/<int:p_id>/electrolysis/plot", methods=["GET"])
def el_plot(p_id):
    key = (p_id, "el")

    data = LAST_RESULTS.get(key)

    if data is None:
        return Response(error_plot("No Electrolysis Data"), mimetype="image/png")

    t, i = data

    img = make_plot(t, i, f"Electrolysis P{p_id}", "Time", "Current")

    LAST_RESULTS.pop(key, None)

    return Response(img, mimetype="image/png")


# -----------------------------------
# RUN SERVER
# -----------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5015, debug=True, threaded=True)