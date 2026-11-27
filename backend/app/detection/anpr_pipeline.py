import cv2
from pathlib import Path
from ultralytics import YOLO

from app.ocr.reader import read_plate
from app.verification.plate_validator import validate_plate
from app.database.db import save_detection
from app.database.vehicle_manager import generate_vehicle_report

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "weights" / "license-plate-finetune-v1n.pt"
IMAGE_PATH = BASE_DIR / "test_images" / "car.jpg"
RESULT_DIR = BASE_DIR / "results"

RESULT_DIR.mkdir(exist_ok=True)


def run_anpr(image_path=None):

    detections = []

    print("\n========== ANPR-X INTELLIGENCE SYSTEM ==========")

    model = YOLO(str(MODEL_PATH))

    input_path = Path(image_path) if image_path else IMAGE_PATH
    image = cv2.imread(str(input_path))

    if image is None:
        print("ERROR: Image not found!")
        return

    results = model.predict(
        source=image,
        conf=0.25,
        imgsz=640,
        device=0,
        save=False
    )

    plate_count = 0

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            detection_confidence = float(box.conf[0])

            plate_crop = image[y1:y2, x1:x2].copy()

            if plate_crop.size == 0:
                continue

            plate_count += 1

            enhanced = cv2.resize(
                plate_crop,
                None,
                fx=2,
                fy=2,
                interpolation=cv2.INTER_CUBIC
            )

            ocr_results = read_plate(enhanced)

            raw_text = "".join(
                item["text"] for item in ocr_results
            )

            ocr_confidence = (
                sum(item["confidence"] for item in ocr_results)
                / len(ocr_results)
                if ocr_results else 0
            )

            validation = validate_plate(raw_text)
            detection_data = {
    "raw_text": raw_text,
    "registration_number": validation["cleaned"],
    "detection_confidence": round(detection_confidence, 4),
    "ocr_confidence": round(ocr_confidence, 4),
    "validation": validation,
    "vehicle_found": False,
    "vehicle": None
}
            print(f"\n========== PLATE {plate_count} ==========")
            print("Extracted:", raw_text)
            print("Cleaned:", validation["cleaned"])
            print(f"Detection confidence: {detection_confidence:.2%}")
            print(f"OCR confidence: {ocr_confidence:.2%}")
            print("Format status:", validation["message"])

            if validation["valid_format"]:

                registration = validation["cleaned"]

                save_detection(
                    registration,
                    detection_confidence,
                    ocr_confidence
                )

                report = generate_vehicle_report(registration)

                if report["found"]:
                    detection_data["vehicle_found"] = True
                    detection_data["vehicle"] = vehicle
                    vehicle = report["vehicle"]

                    print("\n========== VEHICLE INTELLIGENCE ==========")
                    print("Manufacturer:", vehicle["manufacturer"])
                    print("Model:", vehicle["model"])
                    print("Owner:", vehicle["owner_name"])
                    print("Total Challans:",
                          vehicle["traffic_intelligence"]["total_challans"])
                    print("Pending Challans:",
                          vehicle["traffic_intelligence"]["pending_challans"])
                    print("Demo Intelligence Score:",
                          vehicle["intelligence_score"])
                    print("Demo Traffic Category:",
                          vehicle["risk_category"])

                else:
                    print("\nVehicle not found in ANPR-X sample database.")

            else:
                print("\nRegistration format not recognized. Database lookup skipped.")
            detections.append(detection_data)
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                3
            )

            cv2.putText(
                image,
                validation["cleaned"] or "Unreadable",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    output_path = RESULT_DIR / f"anpr_result_{input_path.stem}.jpg"
    cv2.imwrite(str(output_path), image)

    print("\n========== FINAL SUMMARY ==========")
    print("Plates detected:", plate_count)
    print("Annotated image:", output_path)

    return {
    "total_plates_detected": plate_count,
    "detections": detections,
    "result_image": str(output_path)
}
if __name__ == "__main__":

    run_anpr()