import easyocr

reader = easyocr.Reader(['en'])

result = reader.readtext('uploads/Screenshot 2026-06-23 194544.png')

print("\nExtracted Text:\n")

for item in result:
    print(item[1])