import socket
import threading
import random

HOST = "0.0.0.0"
PORT = 5010

# Simulated parameters
adc_min = 200
adc_max = 800


def format_response(msg):
    return f"[DEBUG] Ph meter {msg}\n"


def process_command(cmd):
    cmd = cmd.strip()
    
    if cmd == "1":
        sensor_value = random.randint(adc_min, adc_max)
        response = f"Received cmd {cmd} | ADC value: {sensor_value}"
    elif cmd in ["status", "/", "info"]:
        return format_response("dummy server running!")
    else:
        response = f"Received cmd {cmd} | Unknown command"
    
    print(f"[DEBUG] PLC | {response}")
    return format_response(response)


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
            msg = response.encode()
            #print(msg)
            conn.sendall(msg)
            
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")
        


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] pH meter dummy TCP server at {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
