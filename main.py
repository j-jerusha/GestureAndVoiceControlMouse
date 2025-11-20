from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import subprocess
import os
import sys

app = FastAPI()

# Enable CORS so your front-end can call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve your front-end page
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

# Run Gesture Control
@app.post("/run-gesture")
def run_gesture():
    try:
        script_path = os.path.join(os.path.dirname(__file__), "gestureflow.py")
        subprocess.Popen([sys.executable, script_path])
        return {"message": "Gesture control started successfully!"}
    except Exception as e:
        return {"message": f"Error in gesture: {str(e)}"}
