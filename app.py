from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "id_card" not in request.files:
        return "No file uploaded"

    file = request.files["id_card"]

    if file.filename == "":
        return "No file selected"

    # Save uploaded file
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "uploaded_id.jpg"
    )

    file.save(filepath)

    return render_template(
        "result.html",
        message="ID Card Uploaded Successfully",
        filename="uploaded_id.jpg"
    )


if __name__ == "__main__":
    app.run(debug=True)