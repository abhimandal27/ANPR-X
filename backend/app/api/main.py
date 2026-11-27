from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from app.detection.anpr_pipeline import run_anpr
import shutil
import uuid

from app.database.vehicle_manager import generate_vehicle_report
from app.database.db import get_connection

app = FastAPI(
    title="ANPR-X API",
    description="Intelligent Automated Number Plate Recognition System",
    version="1.0.0"
)

# React frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to the frontend origin before deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "project": "ANPR-X",
        "status": "Running",
        "message": "Welcome to ANPR-X API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ANPR-X Backend"
    }


@app.get("/api/vehicle/{registration}")
def vehicle_details(registration: str):

    registration = registration.upper().strip()

    report = generate_vehicle_report(registration)

    if not report["found"]:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found in ANPR-X database"
        )

    return report


@app.get("/api/detections")
def detection_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM detections
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    conn.close()

    return {
        "total": len(records),
        "detections": [dict(row) for row in records]
    }


@app.post("/api/detect")
async def detect_vehicle(file: UploadFile = File(...)):

    allowed_extensions = {".jpg", ".jpeg", ".png"}

    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are supported"
        )

    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = run_anpr(file_path)

        return {
            "status": "success",
            "filename": filename,
            "ai_results": result
        }
    finally:
        await file.close()