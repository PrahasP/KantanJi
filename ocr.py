import easyocr
import cv2

def read_text_from_image(image_path):
    """
    Read text from an image file using EasyOCR and print the extracted text.
    
    Args:
    - image_path (str): Path to the image file.

    Returns:
    - str: The extracted text from the image.
    """
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['ja'])  # Specify languages as needed

    # Read text from the image using EasyOCR
    results = reader.readtext(image_path, text_threshold=0.25, low_text=0.4)
    
    extracted_text = ""
    for (bbox, text, confidence) in results:
        # Optionally filter by confidence if needed
        if confidence > 0.25:
            extracted_text += f"Detected text: {text} (Confidence: {confidence:.2f})\n"
    
    print(extracted_text)  # Print the extracted text to the console
    return extracted_text  # Return the extracted text (optional)
