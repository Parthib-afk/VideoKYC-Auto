from deepface import DeepFace

result = DeepFace.verify(
    img1_path="live_face.jpg",
    img2_path="id_face.jpg",
    enforce_detection=False
)

print("\nVerification Result")
print("-------------------")
print("Verified:", result["verified"])
print("Distance:", result["distance"])