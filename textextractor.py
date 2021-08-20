from PIL import Image, ImageGrab

# Importamos Pytesseract
import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR'
# Abrimos la imagen
im = Image.open("imagenes/capturatexto.png")

# Utilizamos el método "image_to_string"
# Le pasamos como argumento la imagen abierta con Pillow
texto = pytesseract.image_to_string(im)

# Mostramos el resultado
print('-')
print(texto)
print('-')
bbox_used = (525,445,925,700)

with ImageGrab.grab(bbox = bbox_used) as rgba, rgba.convert(mode='RGB') as screenshot:
    texto = pytesseract.image_to_string(screenshot)
    print(texto)
    print('takeda' in texto.lower())
