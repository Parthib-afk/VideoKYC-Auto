from PIL import Image

img = Image.open("id_face.jpg")
print("Image loaded successfully")
print(img.size)