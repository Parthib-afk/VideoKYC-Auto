from flask import Flask, render_template, request
from ocr import extract_text
from face_match import verify_face
from face_detection import extract_face
from database import create_database, save_record
import os

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

    # OCR
    ocr_text = extract_text(id_path)

    # Extract face from uploaded ID
    id_face_path = extract_face(id_path)

    # Face Verification
    verification = verify_face(
        selfie_path,
        id_face_path
    )

    # Save to Database
    save_record(
        ocr_text,
        verification["verified"],
        verification["distance"]
    )

    return render_template(
        "result.html",
        message="Verification Completed Successfully",
        ocr_text=ocr_text,
        verified=verification["verified"],
        distance=verification["distance"]
    )


if __name__ == "__main__":
    app.run(debug=True)