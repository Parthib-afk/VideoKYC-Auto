import cv2
import os


def extract_face(image_path):

    # Load image
    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Image not found.")

    # Load Haar Cascade
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(80, 80)
    )

    if len(faces) == 0:
        raise Exception("No face found in ID Card.")

    # Take the first detected face
    (x, y, w, h) = faces[0]

    face = image[y:y+h, x:x+w]

    output_path = os.path.join(
        "uploads",
        "id_face.jpg"
    )

    cv2.imwrite(output_path, face)

    return output_path


# For testing only
if __name__ == "__main__":

    path = extract_face("uploads/uploaded_id.jpg")

    print("Face saved at:", path)