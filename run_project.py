import subprocess
import sys
import time

# start backend
backend = subprocess.Popen([
    sys.executable, "-m", "uvicorn",
    "backend.main:app",
    "--reload"
])

time.sleep(2)

# start frontend
frontend = subprocess.Popen([
    sys.executable, "-m", "streamlit",
    "run", "frontend/app.py"
])

backend.wait()
frontend.wait()