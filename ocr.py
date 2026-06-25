import easyocr

from document_classifier import classify_document

from field_extractors import (
    extract_aadhaar,
    extract_pan,
    extract_driving_license,
    extract_passport
)

reader = easyocr.Reader(['en'])


def extract_text(image_path):

    # OCR
    result = reader.readtext(image_path)

    extracted_lines = []

    for item in result:
        extracted_lines.append(item[1])

    full_text = "\n".join(extracted_lines)

    # Detect document type
    document_type = classify_document(full_text)

    # Extract fields
    if document_type == "aadhaar":

        data = extract_aadhaar(full_text)

    elif document_type == "pan":

        data = extract_pan(full_text)

    elif document_type == "driving_license":

        data = extract_driving_license(full_text)

    elif document_type == "passport":

        data = extract_passport(full_text)

    else:

        data = {
            "document": "Unknown",
            "name": "Not Found",
            "dob": "Not Found",
            "id_number": "Not Found",
            "address": "Not Found"
        }

    # Add document type
    data["document"] = document_type

    # Add full OCR text
    data["full_text"] = full_text

    return data