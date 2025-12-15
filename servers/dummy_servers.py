import subprocess

# List of server scripts to start
servers = [
    "arm_dummy_server.py", #127.0.0.1:5000
    "echem_dummy_server.py", #127.0.0.1:5001
    "pipette_dummy_server.py", #127.0.0.1:5002
    "solid_dispensing_dummy_server.py", #127.0.0.1:5003
    "liquid_dispensing_dummy_server.py", #127.0.0.1:5004
    "camera_dummy_server.py", #127.0.0.1:5005
    "top_carousel_dummy_server.py", #127.0.0.1:5006
    "bottom_carousel_dummy_server.py", #127.0.0.1:5007
    "plc_dummy_server.py", #127.0.0.1:5008
    "pipette_aux_dummy_server.py", #127.0.0.1:5009
    "ph_dummy_server.py", #127.0.0.1:5010
    "pumps_dummy_server.py", #127.0.0.1:5011
    "echem_aux_dummy_server.py" #127.0.0.1:5012
]

processes = []

try:
    for server in servers:
        print(f"Starting {server}...")
        p = subprocess.Popen(["python", server])
        processes.append(p)

    print("All dummy servers started. Press Ctrl+C to stop.")
    for p in processes:
        p.wait()

except KeyboardInterrupt:
    print("\nStopping all servers...")
    for p in processes:
        p.terminate()
