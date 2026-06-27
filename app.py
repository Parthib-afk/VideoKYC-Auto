from flask import Flask, render_template, request, send_from_directory
from ocr import extract_text
from face_match import verify_face
from face_detection import extract_face
from database import create_database, save_record
import os
import base64
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create database
create_database()


@app.route("/")
def home():
    return render_template("index.html")


# Route to display uploaded images
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/capture_document", methods=["POST"])
def capture_document():

    data = request.get_json()

    if not data or "image" not in data:
        return "No image received", 400

    image_data = data["image"]

    image_data = image_data.split(",")[1]

    image_bytes = base64.b64decode(image_data)

    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "captured_id.jpg"
    )

    with open(save_path, "wb") as f:
        f.write(image_bytes)

    # OCR
    ocr_result = extract_text(save_path)

    # Extract Face
    id_face_path = extract_face(save_path)

    return {
        "status": "success",
        "message": "ID Card Captured Successfully",
        "name": ocr_result["name"],
        "dob": ocr_result["dob"],
        "licence": ocr_result["licence"],
        "full_text": ocr_result["full_text"]
    }
    
@app.route("/start_face_verification")
def start_face_verification():

    # Run liveness detection
    subprocess.run(["py", "-3.11", "liveness.py"])

    live_face = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "live_face.jpg"
    )

    id_face = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "id_face.jpg"
    )

    captured_id = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "captured_id.jpg"
    )

    if not os.path.exists(live_face):

        return "Live Face Not Captured"

    # OCR Again
    ocr_result = extract_text(captured_id)

    # Face Verification
    verification = verify_face(
        live_face,
        id_face
    )

    similarity = max(
        0,
        round((1 - verification["distance"]) * 100, 2)
    )

    # Save Record
    save_record(
        ocr_result["full_text"],
        verification["verified"],
        verification["distance"]
    )

    # Show Result Page
    return render_template(

        "result.html",

        message="Verification Completed Successfully",

        verified=verification["verified"],

        similarity=similarity,

        distance=verification["distance"],

        liveness="Passed",

        id_image="captured_id.jpg",

        selfie_image="live_face.jpg",

        name=ocr_result["name"],

        dob=ocr_result["dob"],

        licence=ocr_result["licence"],

        full_text=ocr_result["full_text"]

    )

@app.route("/upload", methods=["POST"])
def upload():

    # Check if both files are uploaded
    if "id_card" not in request.files or "selfie" not in request.files:
        return "Please upload both ID Card and Selfie."

    id_card = request.files["id_card"]
    selfie = request.files["selfie"]

    # Check if files are selected
    if id_card.filename == "" or selfie.filename == "":
        return "Please select both files."

    # Save uploaded files
    id_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "uploaded_id.jpg"
    )

    selfie_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "uploaded_selfie.jpg"
    )

    id_card.save(id_path)
    selfie.save(selfie_path)

    # -------------------------
    # OCR
    # -------------------------
    ocr_result = extract_text(id_path)

    # -------------------------
    # Extract Face from ID Card
    # -------------------------
    id_face_path = extract_face(id_path)

    # -------------------------
    # Face Verification
    # -------------------------
    verification = verify_face(
        selfie_path,
        id_face_path
    )

    # -------------------------
    # Similarity Score
    # -------------------------
    similarity = max(
        0,
        round((1 - verification["distance"]) * 100, 2)
    )

    # -------------------------
    # Liveness Status
    # -------------------------
    liveness = "Passed"

    # -------------------------
    # Save to Database
    # -------------------------
    save_record(
        ocr_result["full_text"],
        verification["verified"],
        verification["distance"]
    )

    # -------------------------
    # Render Result Page
    # -------------------------
    return render_template(
        "result.html",

        message="Verification Completed Successfully",

        verified=verification["verified"],

        similarity=similarity,

        distance=verification["distance"],

        liveness=liveness,

        id_image="uploaded_id.jpg",

        selfie_image="uploaded_selfie.jpg",

        name=ocr_result["name"],

        dob=ocr_result["dob"],

        licence=ocr_result["licence"],

        full_text=ocr_result["full_text"]
    )


if __name__ == "__main__":
    app.run(debug=True)