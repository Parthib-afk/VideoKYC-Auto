import easyocr
import re

# Initialize EasyOCR
reader = easyocr.Reader(['en'])


def extract_text(image_path):

    result = reader.readtext(image_path)

    extracted_text = []

    for item in result:
        extracted_text.append(item[1])

    full_text = "\n".join(extracted_text)

    # -----------------------------
    # Default Values
    # -----------------------------

    name = "Not Found"
    dob = "Not Found"
    licence_number = "Not Found"

    # -----------------------------
    # Date of Birth
    # -----------------------------

    dob_pattern = r"\d{2}[/-]\d{2}[/-]\d{4}"

    dob_match = re.search(dob_pattern, full_text)

    if dob_match:
        dob = dob_match.group()

    # -----------------------------
    # Driving Licence Number
    # -----------------------------

    licence_pattern = r"[A-Z]{2}\d{2}\s?\d{11}|[A-Z]{2}-\d{2}-\d{11}"

    licence_match = re.search(
        licence_pattern,
        full_text.replace("\n", " ")
    )

    if licence_match:
        licence_number = licence_match.group()

    # -----------------------------
    # Guess Name
    # -----------------------------

    ignore_words = [
        "DRIVING",
        "LICENCE",
        "LICENSE",
        "INDIA",
        "TRANSPORT",
        "GOVERNMENT",
        "DOB",
        "DL",
        "VALID",
        "AUTHORITY",
        "ADDRESS",
        "DATE",
        "BIRTH"
    ]

    lines = full_text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) < 3:
            continue

        words = line.split()

        if len(words) < 2:
            continue

        if line.upper() != line:
            continue

        valid = True

        for word in ignore_words:

            if word in line.upper():

                valid = False

                break

        if valid:

            name = line.title()

            break

    # -----------------------------
    # Return Dictionary
    # -----------------------------

    return {

        "name": name,

        "dob": dob,

        "licence": licence_number,

        "full_text": full_text

    }