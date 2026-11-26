import easyocr

print("Initializing ANPR-X OCR Engine...")

reader = easyocr.Reader(
    ['en'],
    gpu=True
)

def read_plate(plate_image):

    results = reader.readtext(
        plate_image,
        detail=1,
        paragraph=False,
        allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )

    detected_text = []

    for bbox, text, confidence in results:
        detected_text.append({
            "text": text,
            "confidence": round(float(confidence), 4)
        })

    return detected_text