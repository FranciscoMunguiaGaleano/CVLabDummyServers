import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 5014



def format_response(text):
    return f"[DEBUG] Toledo pH meter aux {text}\n"



def process_command(cmd):
    """Process incoming TCP command."""

    cmd = cmd.strip()

    if cmd == "1":
        action = "press button 1"

    elif cmd == "press button 2":
        action = "servo_move_down"

    else:
        action = "invalid_command"

    log = f"Command {cmd} | Action: {action}"
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
