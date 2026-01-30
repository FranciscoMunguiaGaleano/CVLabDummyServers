import socket
import threading


HOST = "0.0.0.0"
PORT = 5009

# Dummy servo states
servo1_pos = 180
servo2_pos = 0
servo_speed = 100


def format_response(msg):
    return f"[DEBUG] Pipette_aux {msg}\n"


def process_command(cmd):
    global servo1_pos, servo2_pos, servo_speed

    cmd = cmd.strip()
    response = f"Received command: {cmd} | "

    if cmd == "1":  # Load pipette
        servo1_pos = 100
        response += f"Loading pipette | servo1={servo1_pos}"

    elif cmd == "2":  # Unload pipette
        servo1_pos = 70
        response += f"Unloading pipette | servo1={servo1_pos}"
        servo1_pos = 180  # Restore position

    elif cmd == "3":  # Eject tip
        servo2_pos = 120
        response += f"Ejecting tip | servo2={servo2_pos}"
        servo2_pos = 0

    elif cmd == "4":  # Reset servos
        start = servo1_pos
        end = 180
        response += f"Returning servo1 from {start} to {end} at speed {servo_speed}"
        servo1_pos = end
        servo2_pos = 0

    elif cmd == "5":
        servo_speed = 100
        response += "Speed set to 100"

    elif cmd == "6":
        servo_speed = 50
        response += "Speed set to 50"

    elif cmd == "7":
        servo_speed = 10
        response += "Speed set to 10"

    elif cmd in ["status", "/", "info"]:
        return format_response("dummy server running!")

    else:
        response += "Error: Unknown command"

    print(f"[DEBUG] Pipette_aux | {response}")
    return format_response(response)


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
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        print(f"[DISCONNECTED] {addr}")
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Pipette dummy TCP server at {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
