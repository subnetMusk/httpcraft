import subprocess
import time
import os
import sys

base = os.path.dirname(__file__)
server_path = os.path.join(base, "mock_saver_server.py")
client_path = os.path.join(base, "test_saving_script.py")

print("[ℹ] Launching mock server in background...")
server = subprocess.Popen([sys.executable, server_path])

try:
    time.sleep(2)  # wait for Flask to start
    print("[ℹ] Running test_saving_script.py...")
    subprocess.run([sys.executable, client_path], check=True)
finally:
    print("[ℹ] Terminating mock server...")
    server.terminate()
    server.wait()
    print("[✔] Done.")