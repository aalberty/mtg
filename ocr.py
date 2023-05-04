import cv2
import pytesseract
import numpy as np

# Set tesseract path if not in your PATH environment variable
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def preprocess_image(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding to binarize the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Dilate to fill in any gaps
    kernel = np.ones((5,5), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    return dilated

def get_card_contours(img):
    # Find contours in the image
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])

    # Group contours into columns
    column_contours = []
    column = []
    prev_x, prev_y, prev_w, prev_h = 0, 0, 0, 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if prev_x == 0:
            column.append(contour)
        elif x > prev_x + prev_w:
            column_contours.append(column)
            column = []
            column.append(contour)
        else:
            column.append(contour)
        prev_x, prev_y, prev_w, prev_h = x, y, w, h

    # Add last column
    column_contours.append(column)

    # Sort contours from top to bottom within each column
    for i in range(len(column_contours)):
        column_contours[i] = sorted(column_contours[i], key=lambda x: cv2.boundingRect(x)[1])

    return column_contours

def extract_text(img):
    # Preprocess the image
    processed = preprocess_image(img)

    # Get the contours of each card
    contours = get_card_contours(processed)

    # Extract text from each card
    cards_text = []
    for column in contours:
        column_text = []
        for contour in column:
            # Get bounding box of contour
            x, y, w, h = cv2.boundingRect(contour)

            # Crop image to bounding box
            card_img = img[y:y+h, x:x+w]

            # Extract text from card
            text = pytesseract.image_to_string(card_img)

            # Add text to column text
            column_text.append(text.strip())

        # Add column text to cards text
        cards_text.append(column_text)

    return cards_text

# Test on sample image
filename = 'sample_cards.jpg'
img = cv2.imread(filename)

cards_text = extract_text(img)

print(cards_text)
