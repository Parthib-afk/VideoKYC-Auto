from PIL import Image

img = Image.open("uploads/id_card.png")
print("Success")
print(img.size)