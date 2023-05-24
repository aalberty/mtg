import cv2

def outline_cards(filepath):
    # Load the image
    image = cv2.imread(filepath)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to convert to binary image
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
        # Find the bounding rectangle of each contour
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / h

        # Only draw the rectangle if it has the aspect ratio of a playing card
        if aspect_ratio > 0.6 and aspect_ratio < 0.9:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image
    cv2.imshow('Playing Cards', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
