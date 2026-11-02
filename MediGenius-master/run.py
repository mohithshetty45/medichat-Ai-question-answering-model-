import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from threading import Thread

VENV_DIR = ".venv"
IS_WINDOWS = sys.platform == "win32"
PYTHON_EXE = os.path.join(VENV_DIR, "Scripts", "python.exe") if IS_WINDOWS else os.path.join(VENV_DIR, "bin", "python")

def setup():
    # Create virtual environment if it doesn't exist
    if not os.path.exists(VENV_DIR):
        print(f"Creating virtual environment in {VENV_DIR}...")
        subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)

    # Auto-install dependencies
    if os.path.exists("backend/requirements.txt"):
        print("Checking backend deps...")
        # Use the venv's python to install requirements
        subprocess.run([PYTHON_EXE, "-m", "pip", "install", "-r", "backend/requirements.txt"])
    
    if not os.path.exists("frontend/node_modules"):
        print("Installing frontend deps...")
        subprocess.run(["npm", "install"], cwd="frontend", shell=True)

def is_api_ready():
    try:
        with urllib.request.urlopen("http://localhost:8000/api/v1/health", timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def wait_for_api():
    print("Waiting for backend...")
    for _ in range(60):
        if is_api_ready():
            print("Backend ready!")
            return True
        time.sleep(2)
    return False

if __name__ == "__main__":
    setup()
    
    env = {**os.environ, "PYTHONPATH": os.path.abspath("backend")}
    if is_api_ready():
        print("Backend is already running on port 8000; reusing it.")
    else:
        # Start backend in background using venv's python.
        Thread(target=lambda: subprocess.run(
            [PYTHON_EXE, "-m", "uvicorn", "app.main:app", "--port", "8000"],
            cwd="backend", env=env
        ), daemon=True).start()

    # Wait and launch frontend
    if wait_for_api():
        subprocess.run(["npm", "run", "dev"], cwd="frontend", shell=True)
