import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.imshow("Capture Face", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        cv2.imwrite("live_face.jpg", frame)
        print("Face Saved Successfully")
        break

cap.release()
cv2.destroyAllWindows()