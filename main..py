import cv2
import re
import numpy as np
import cvzone
from ultralytics import YOLO
from paddleocr import PaddleOCR

from server import manage_numberplate_db


# ============================================================
# INITIALIZATION
# ============================================================

# Initialize PaddleOCR
ocr = PaddleOCR()

# Load video
cap = cv2.VideoCapture("tc.mp4")

# Load YOLO11 TFLite model
model = YOLO("best_float32.tflite")

# Load class names
with open("coco1.txt", "r") as f:
    class_names = f.read().splitlines()


# ============================================================
# OCR FUNCTION
# ============================================================

def perform_ocr(image_array):
    """
    Perform OCR on the cropped number plate image
    and return the detected text.
    """

    if image_array is None or image_array.size == 0:
        return ""

    try:
        results = ocr.ocr(image_array, rec=True)

        detected_text = []

        if results and results[0] is not None:
            for result in results[0]:
                if result and len(result) > 1:
                    text = result[1][0]
                    if text:
                        detected_text.append(text)

        return "".join(detected_text)

    except Exception as e:
        print(f"OCR Error: {e}")
        return ""


# ============================================================
# CLEAN NUMBER PLATE TEXT
# ============================================================

def clean_plate_text(text):
    """
    Clean OCR output so that unnecessary characters
    are removed before storing the number plate.
    """

    if not text:
        return ""

    # Convert to uppercase
    text = text.upper()

    # Remove unwanted characters
    text = re.sub(r"[^A-Z0-9]", "", text)

    return text


# ============================================================
# MOUSE CALLBACK
# ============================================================

def RGB(event, x, y, flags, param):
    """
    Display mouse coordinates when the mouse moves
    over the video window.
    """

    if event == cv2.EVENT_MOUSEMOVE:
        print([x, y])


# ============================================================
# WINDOW SETUP
# ============================================================

cv2.namedWindow("RGB")
cv2.setMouseCallback("RGB", RGB)


# ============================================================
# ROI / COUNTER SETUP
# ============================================================

count = 0

# Region of Interest
area = [
    (5, 180),
    (3, 249),
    (984, 237),
    (950, 168)
]

# Stores vehicle tracking IDs that have already been counted
counter = []


# ============================================================
# MAIN VIDEO LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    # Stop when video ends
    if not ret:
        break

    # Resize frame
    frame = cv2.resize(frame, (1020, 500))

    # ========================================================
    # YOLO11 TRACKING
    # ========================================================

    results = model.track(
        frame,
        persist=True,
        imgsz=240
    )

    # Check whether tracking information is available
    if (
        results[0].boxes is not None
        and results[0].boxes.id is not None
    ):

        boxes = results[0].boxes.xyxy.int().cpu().tolist()
        class_ids = results[0].boxes.cls.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        confidences = results[0].boxes.conf.cpu().tolist()

        # ====================================================
        # PROCESS EACH DETECTED OBJECT
        # ====================================================

        for box, class_id, track_id, conf in zip(
            boxes,
            class_ids,
            track_ids,
            confidences
        ):

            # Make sure class ID is valid
            if class_id >= len(class_names):
                continue

            class_name = class_names[class_id]

            x1, y1, x2, y2 = box

            # Calculate center point of detected object
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # =================================================
            # CHECK WHETHER CENTER IS INSIDE ROI
            # =================================================

            result = cv2.pointPolygonTest(
                np.array(area, np.int32),
                (cx, cy),
                False
            )

            if result >= 0:

                # =================================================
                # PROCESS ONLY NEW TRACK IDs
                # =================================================

                if track_id not in counter:

                    counter.append(track_id)

                    # =============================================
                    # CROP DETECTED NUMBER PLATE
                    # =============================================

                    crop = frame[y1:y2, x1:x2]

                    if crop.size == 0:
                        continue

                    crop = cv2.resize(
                        crop,
                        (120, 70)
                    )

                    # =============================================
                    # OCR
                    # =============================================

                    text = perform_ocr(crop)

                    print("OCR Result:", text)

                    # =============================================
                    # CLEAN OCR RESULT
                    # =============================================

                    text = clean_plate_text(text)

                    print("Cleaned Plate:", text)

                    # =============================================
                    # SAVE TO DATABASE
                    # =============================================

                    if text:
                        try:
                            manage_numberplate_db(text)
                            print(
                                f"Number plate '{text}' "
                                "saved successfully."
                            )

                        except Exception as e:
                            print(
                                f"Database Error: {e}"
                            )

    # ========================================================
    # DISPLAY TOTAL COUNT
    # ========================================================

    mycounter = len(counter)

    cvzone.putTextRect(
        frame,
        f"Vehicles: {mycounter}",
        (50, 60),
        1,
        1
    )

    # ========================================================
    # DRAW ROI
    # ========================================================

    cv2.polylines(
        frame,
        [np.array(area, np.int32)],
        True,
        (255, 0, 0),
        2
    )

    # ========================================================
    # DISPLAY FRAME
    # ========================================================

    cv2.imshow("RGB", frame)

    # Press ESC to exit
    # waitKey(1) allows the video to continue playing
    if cv2.waitKey(1) & 0xFF == 27:
        break


# ============================================================
# RELEASE RESOURCES
# ============================================================

cap.release()
cv2.destroyAllWindows()
