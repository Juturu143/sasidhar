import cv2

# Load image
image = cv2.imread("car.jpg")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load Haar cascade for number plate detection
plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_russian_plate_number.xml")

# Detect plates
plates = plate_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in plates:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Show result
cv2.imshow("License Plate Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()