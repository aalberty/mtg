import cv2
import pytesseract

def ocr_core(filename):
    # Load the image using OpenCV
    img = cv2.imread(filename)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create a binary image
    binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Apply denoising to remove noise from the image
    denoised = cv2.medianBlur(binary, 3)

    # Apply deskewing to correct the orientation of the text
    coords = cv2.findNonZero(denoised)
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = denoised.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(denoised, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # Perform OCR on the transformed image
    text = pytesseract.image_to_string(rotated)

    # Return the OCR result as a string
    return text
