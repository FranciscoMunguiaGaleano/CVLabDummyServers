import socket
import threading
import time
import random

HOST = "0.0.0.0"
PORT = 5011

# ─── Simulated states ──────────────────────────────────────
lift_moving = False
lift_start_time = None
lift_duration = 3000  # ms
shaker_on_state = False
pumps_on_state = False
emergency_triggered = False

# Lift control pins (simulated)
lift_en = False
lift_dir = False  # False = down, True = up

# Simulated display bitmaps
bitmaps = {
    "frame_1": "[Lift / shaker / pumps → ON]",
    "frame_2": "[Lift / shaker / pumps → OFF]",
    "frame_3": "[Emergency → TRIGGERED]",
    "frame_4": "[Emergency → NOT triggered]",
    "frame_ok": "[Motion OK / idle]",
    "frame_err": "[ERROR]"
}


def format_response(text):
    return f"[DEBUG] Pumps {text}\n"


def check_lift_motion():
    """Simulates completion of lift motion after lift_duration."""
    global lift_moving, lift_en, lift_dir
    if lift_moving and lift_start_time:
        if int(time.time() * 1000) - lift_start_time > lift_duration:
            lift_moving = False
            lift_en = False
            lift_dir = False
            print(format_response("Lift motion complete | Bitmap: " + bitmaps["frame_ok"]).strip())


def process_command(cmd):
    global lift_moving, lift_start_time, shaker_on_state, pumps_on_state
    global lift_en, lift_dir, emergency_triggered

    cmd = cmd.strip()
    check_lift_motion()

    if cmd == "1":  # Lift Down
        lift_en = True
        lift_dir = False
        lift_moving = True
        lift_start_time = int(time.time() * 1000)
        action = "lift_down"
        bitmap = bitmaps["frame_1"]

    elif cmd == "2":  # Lift Up
        lift_en = False  # Simulated differently from original but safe
        lift_dir = True
        lift_moving = True
        lift_start_time = int(time.time() * 1000)
        action = "lift_up"
        bitmap = bitmaps["frame_2"]

    elif cmd == "3":  # Shaker ON
        shaker_on_state = True
        action = "shaker_on"
        bitmap = bitmaps["frame_1"]

    elif cmd == "4":  # Shaker OFF
        shaker_on_state = False
        action = "shaker_off"
        bitmap = bitmaps["frame_2"]

    elif cmd == "5":  # Pumps ON
        pumps_on_state = True
        action = "pumps_on"
        bitmap = bitmaps["frame_1"]

    elif cmd == "6":  # Pumps OFF
        pumps_on_state = False
        action = "pumps_off"
        bitmap = bitmaps["frame_2"]

    elif cmd == "7":  # Emergency Check
        emergency_triggered = random.choice([True, False])
        action = "emergency_status"
        bitmap = bitmaps["frame_3"] if emergency_triggered else bitmaps["frame_4"]

    elif cmd == "8":  # Stop Lift
        lift_en = False
        lift_dir = False
        lift_moving = False
        action = "lift_stop"
        bitmap = bitmaps["frame_ok"]
    elif cmd in ["status", "/", "info"]:
        return format_response("dummy server running!")

    else:
        action = "invalid_command"
        bitmap = bitmaps["frame_err"]

    log = f"Command: {cmd} | Action: {action} | Bitmap: {bitmap}"
    print(format_response(log).strip())
    return format_response(log)


def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            cmd = data.decode().strip()
            print(f"[RECEIVED from {addr}] '{cmd}'")
            response = process_command(cmd)
            conn.sendall(response.encode())
    finally:
        print(f"[DISCONNECTED] {addr}")
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Lift/Shaker/Pump dummy TCP server at {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
