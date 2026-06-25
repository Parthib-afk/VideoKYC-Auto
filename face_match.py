from deepface import DeepFace


def verify_face(selfie_path, id_face_path):

    result = DeepFace.verify(
        img1_path=selfie_path,
        img2_path=id_face_path,
        enforce_detection=False
    )

    return {
        "verified": result["verified"],
        "distance": result["distance"]
    }


# For testing only
if __name__ == "__main__":

    verification = verify_face(
        "uploads/uploaded_selfie.jpg",
        "uploads/id_face.jpg"
    )

    print("\nVerification Result")
    print("-----------------------")
    print("Verified :", verification["verified"])
    print("Distance :", verification["distance"])