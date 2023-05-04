import pytesseract
from PIL import Image

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    # Open the image file using Pillow
    with Image.open(filename) as img:
        # Use pytesseract to convert the image into a string
        text = pytesseract.image_to_string(img)
        return text