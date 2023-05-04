import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return thresh

def extract_text(img):
    cards_text = []
    processed = preprocess_image(img)
    contours, hierarchy = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:
            card = img[y:y+h, x:x+w]
            card_text = pytesseract.image_to_string(card)
            cards_text.append(card_text.strip())
    return cards_text

filename = 'sample_cards.jpg'
img = cv2.imread(filename)
cards_text = extract_text(img)
print(cards_text)
