import cv2
import numpy as np
import numpy as np
import pytesseract
from pdf2image import convert_from_path

def crop(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # Adjust kernel size
    dilated = cv2.dilate(binary, kernel, iterations=10)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_width = 0
    best_rect = None
    max_allowed_width = int(0.8 * image.shape[1]) 

    for contour in contours:
        if cv2.contourArea(contour) > 100000: 
            x, y, w, h = cv2.boundingRect(contour)
            if w > max_width and w < max_allowed_width: 
                max_width = w
                best_rect = (x, y, w, h)

    # Recortar la imagen
    if best_rect is not None:
        x, y, w, h = best_rect
        cropped_image = image[:, x:x + w]
        return cropped_image
    else:
        print("No suitable paragraph found.")


def extract_text(pdf_file):
    pages = convert_from_path(pdf_file)
    extracted_text = []

    for page in pages:

        preprocessed_image = crop(np.array(page))
        try:
        #Extraer el texto
            text = pytesseract.image_to_string(preprocessed_image)
            extracted_text.append(text)
        except Exception as e:
            print(f"Error processing page: {e}")
            continue

        full_text = "\n".join(extracted_text)
    return full_text
