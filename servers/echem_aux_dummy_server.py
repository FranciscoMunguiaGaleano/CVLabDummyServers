import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5012

# Simulated states
servo1_pos = 90  # Default neutral position
motorA_running = False
motorB_running = False
speed_mode = "medium"

# Bitmap simulation (just console output)
bitmaps = {
    "frame_1": "[Servo → Position A]",
    "frame_2": "[Servo → Position B]",
    "frame_3": "[Motor A → ON]",
    "frame_4": "[Motor A → OFF]",
    "frame_ok": "[Motor B → OK]",
    "frame_err": "[ERROR]"
}


def format_response(text):
    return f"[DEBUG] Echem aux {text}\n"


def move_servo_smooth(start, end, delay_ms=10):
    """Simulates smooth servo travel like moveServoSmooth(...)."""
    global servo1_pos
    step = 1 if end > start else -1
    for pos in range(start, end, step):
        servo1_pos = pos
        time.sleep(delay_ms / 1000.0)
    servo1_pos = end


def process_command(cmd):
    """Process incoming TCP command."""
    global servo1_pos, motorA_running, motorB_running, speed_mode

    cmd = cmd.strip()

    if cmd == "1":
        move_servo_smooth(servo1_pos, 179, 10)
        action = "servo_move_up"
        bitmap = bitmaps["frame_1"]

    elif cmd == "2":
        move_servo_smooth(servo1_pos, 8, 10)
        action = "servo_move_down"
        bitmap = bitmaps["frame_2"]

    elif cmd == "3":
        motorA_running = True
        action = "motorA_on"
        bitmap = bitmaps["frame_3"]

    elif cmd == "4":
        motorA_running = False
        action = "motorA_off"
        bitmap = bitmaps["frame_4"]

    elif cmd == "5":
        motorB_running = True
        action = "motorB_on"
        bitmap = bitmaps["frame_ok"]

    elif cmd == "6":
        motorB_running = False
        action = "motorB_off"
        bitmap = bitmaps["frame_ok"]

    elif cmd == "7":
        speed_mode = "slow"
        action = "set_speed_slow"
        bitmap = bitmaps["frame_ok"]

    elif cmd == "8":
        speed_mode = "medium"
        action = "set_speed_medium"
        bitmap = bitmaps["frame_ok"]

    elif cmd == "9":
        speed_mode = "fast"
        action = "set_speed_fast"
        bitmap = bitmaps["frame_ok"]

    elif cmd in ["status", "/", "info"]:
        return format_response("dummy server running!")

    else:
        action = "invalid_command"
        bitmap = bitmaps["frame_err"]

    log = f"Command {cmd} | Action: {action} | Bitmap: {bitmap}"
    print(format_response(log).strip())
    return format_response(log)


def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            cmd = data.decode()
            print(f"[RECEIVED from {addr}] '{cmd.strip()}'")
            response = process_command(cmd)
            conn.sendall(response.encode())
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Polisher dummy TCP server at {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
