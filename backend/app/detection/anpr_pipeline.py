import cv2
from pathlib import Path
from ultralytics import YOLO

from app.ocr.reader import read_plate

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "weights" / "license-plate-finetune-v1n.pt"
IMAGE_PATH = BASE_DIR / "test_images" / "car.jpg"
RESULT_DIR = BASE_DIR / "results"

RESULT_DIR.mkdir(exist_ok=True)


def run_anpr():

    print("\n========== ANPR-X ==========")

    model = YOLO(str(MODEL_PATH))

    image = cv2.imread(str(IMAGE_PATH))

    if image is None:
        print("ERROR: Image not found!")
        return

    results = model.predict(
        source=image,
        conf=0.25,
        imgsz=640,
        device=0
    )

    plate_count = 0

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = map(
                int, box.xyxy[0].tolist()
            )

            confidence = float(box.conf[0])

            # Crop from ORIGINAL image
            plate_crop = image[y1:y2, x1:x2].copy()

            if plate_crop.size == 0:
                continue

            plate_count += 1

            # Save original crop
            crop_path = RESULT_DIR / f"plate_{plate_count}.jpg"
            cv2.imwrite(str(crop_path), plate_crop)

            # Upscale for OCR
            enhanced = cv2.resize(
                plate_crop,
                None,
                fx=2,
                fy=2,
                interpolation=cv2.INTER_CUBIC
            )

            # Read registration number
            ocr_results = read_plate(enhanced)

            plate_text = " ".join(
                item["text"] for item in ocr_results
            )

            print(f"\nPlate {plate_count}")
            print(f"Detection confidence: {confidence:.2%}")
            print(f"Extracted text: {plate_text}")

            for item in ocr_results:
                print(
                    f"  OCR confidence: "
                    f"{item['confidence']:.2%}"
                )

            # Draw bounding box
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                3
            )

            cv2.putText(
                image,
                plate_text or "Unreadable",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    output_path = RESULT_DIR / "anpr_result.jpg"

    cv2.imwrite(str(output_path), image)

    print("\n========== SUMMARY ==========")
    print("Plates detected:", plate_count)
    print("Result saved:", output_path)


if __name__ == "__main__":
    run_anpr()