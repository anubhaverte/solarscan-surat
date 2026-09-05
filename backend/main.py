from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "rooftop_results.json")
HTML_PATH = os.path.normpath(os.path.join(BASE_DIR, "..", "Frontend", "index.html"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load once at startup -> fast + you instantly see in terminal if data is OK
ROOFTOPS = None
LOAD_ERROR = None
try:
    with open(JSON_PATH, encoding="utf-8") as f:
        ROOFTOPS = json.load(f)
    print(f"LOADED {len(ROOFTOPS)} rooftops from {JSON_PATH}")
except Exception as e:
    LOAD_ERROR = str(e)
    print(f"FAILED to load rooftop_results.json: {e}")

@app.get("/")
def root():
    if os.path.exists(HTML_PATH):
        return FileResponse(HTML_PATH)
    return {"status": "SolarScan Surat API is running"}

@app.get("/rooftops")
def get_rooftops():
    if ROOFTOPS is None:
        return JSONResponse(status_code=500, content={"error": LOAD_ERROR})
    return ROOFTOPS