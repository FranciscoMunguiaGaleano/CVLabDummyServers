import socket
import threading

HOST = "0.0.0.0"  # listen on all interfaces
PORT = 5008

# Simulated current relay states
relay_state = {}

def format_response(msg):
    return f"[DEBUG] PLC {msg}\n"

def process_command(cmd):
    cmd = cmd.strip().lower()

    # Matches "main1" → ON
    if cmd.startswith("main") and cmd[4:].isdigit():
        n = cmd[4:]
        relay_state[f"main{n}"] = "ON"
        return format_response(f"Main relay {n} turned ON.")
    
    # Matches "mainoff1" → OFF
    if cmd.startswith("mainoff") and cmd[7:].isdigit():
        n = cmd[7:]
        relay_state[f"main{n}"] = "OFF"
        return format_response(f"Main relay {n} turned OFF.")
    
    # Matches "ext1" → ON
    if cmd.startswith("ext") and cmd[3:].isdigit():
        n = cmd[3:]
        relay_state[f"ext{n}"] = "ON"
        return format_response(f"External relay {n} turned ON.")
    
    # Matches "offext1" → OFF
    if cmd.startswith("offext") and cmd[6:].isdigit():
        n = cmd[6:]
        relay_state[f"ext{n}"] = "OFF"
        return format_response(f"External relay {n} turned OFF.")

    if cmd in ["status", "/", "info"]:
        return format_response("dummy server running!")

    return format_response(f"Unknown command: '{cmd}'")

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
        data = conn.recv(1024)
        if data:
            cmd = data.decode().strip()
            print(f"[RECEIVED from {addr}] '{cmd}'")
            response = process_command(cmd)
            conn.sendall(response.encode())
    except ConnectionResetError:
        pass
    finally:
        print(f"[DISCONNECTED] {addr}")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] PLC dummy TCP server at {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()

