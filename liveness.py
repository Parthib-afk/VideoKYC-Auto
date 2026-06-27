import cv2
import mediapipe as mp
import math

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

cap = cv2.VideoCapture(0)

blink_count = 0
blink_detected = False

left_done = False
right_done = False


def distance(p1, p2):

    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


while True:

    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        landmarks = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        # -------------------------
        # Face Bounding Box
        # -------------------------

        xs = [lm.x for lm in landmarks.landmark]
        ys = [lm.y for lm in landmarks.landmark]

        x1 = int(min(xs) * w)
        y1 = int(min(ys) * h)

        x2 = int(max(xs) * w)
        y2 = int(max(ys) * h)

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0,255,0),
            3
        )

        # -------------------------
        # Blink Detection
        # -------------------------

        top = landmarks.landmark[159]
        bottom = landmarks.landmark[145]

        eye_open = distance(top, bottom)

        if eye_open < 0.010 and not blink_detected:

            blink_count += 1
            blink_detected = True

        if eye_open > 0.015:

            blink_detected = False

        # -------------------------
        # Head Turn Detection
        # -------------------------

        nose = landmarks.landmark[1]

        if nose.x < 0.40:
            left_done = True

        if nose.x > 0.60:
            right_done = True

        # -------------------------
        # Status
        # -------------------------

        cv2.putText(
            frame,
            f"Blink: {blink_count}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"Left: {left_done}",
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,0,0),
            2
        )

        cv2.putText(
            frame,
            f"Right: {right_done}",
            (20,120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,0,0),
            2
        )

        # -------------------------
        # Liveness Passed
        # -------------------------

        if blink_count >= 1 and left_done and right_done:

            cv2.putText(
                frame,
                "LIVENESS PASSED",
                (100,170),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                3
            )

            cv2.imwrite(
                "uploads/live_face.jpg",
                frame
            )

            print("Liveness Passed")
            print("Live Face Saved")

            cv2.imshow("Liveness Detection", frame)

            cv2.waitKey(2000)

            break

    cv2.imshow("Liveness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()