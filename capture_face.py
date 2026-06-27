import cv2
import os

# Load Haar Cascade Face Detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

# Create uploads folder if it doesn't exist
os.makedirs("uploads", exist_ok=True)

print("Press 'S' to capture the face.")
print("Press 'Q' to quit.")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    # Draw green rectangle around detected face
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

    # Status text
    if len(faces) == 0:

        cv2.putText(
            frame,
            "No Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    else:

        cv2.putText(
            frame,
            "Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Live Face Verification", frame)

    key = cv2.waitKey(1) & 0xFF

    # Save face
    if key == ord('s'):

        cv2.imwrite(
            "uploads/live_face.jpg",
            frame
        )

        print("Live Face Saved Successfully")

        break

    # Quit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()