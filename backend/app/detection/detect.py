import cv2
from pathlib import Path
from ultralytics import YOLO

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "weights" / "license-plate-finetune-v1n.pt"
IMAGE_PATH = BASE_DIR / "test_images" / "car.jpg"
RESULT_DIR = BASE_DIR / "results"

RESULT_DIR.mkdir(exist_ok=True)

def detect_number_plate():

    print("Loading ANPR-X detection model...")

    model = YOLO(str(MODEL_PATH))

    image = cv2.imread(str(IMAGE_PATH))

    if image is None:
        print("ERROR: Could not load vehicle image.")
        return

    print("Detecting number plates...")

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
            confidence = float(box.conf[0])

            plate_count += 1

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
                f"Plate: {confidence:.2f}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )

            # Crop detected plate
            plate_crop = image.copy()[y1:y2, x1:x2]

            cv2.imwrite(
                str(RESULT_DIR / f"plate_{plate_count}.jpg"),
                plate_crop
            )

    # Save annotated image
    output_path = RESULT_DIR / "detection_result.jpg"
    cv2.imwrite(str(output_path), image)

    print(f"\nDetection completed!")
    print(f"Number plates detected: {plate_count}")
    print(f"Result saved: {output_path}")

if __name__ == "__main__":
    detect_number_plate()