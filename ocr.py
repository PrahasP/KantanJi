import easyocr
import kanji_simplifier

def read_text_from_image(image_path):
    """
    Read text from an image file using EasyOCR and print the extracted text.
    
    Args:
    - image_path (str): Path to the image file.

    Returns:
    - str: The extracted text from the image.
    """
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['ja'], gpu= True)  # Specify languages as needed

    # Read text from the image using EasyOCR
    results = reader.readtext(image_path, text_threshold=0.25, low_text=0.4)
    
    extracted_text = ""
    for (bbox, text, confidence) in results:
        # Optionally filter by confidence if needed
        if confidence > 0.25:
            extracted_text += f"{text}\n"
    
    simplified_text = kanji_simplifier.KanjiSimplifier.generate_furigana(extracted_text)

    return "Extracted Text:\n" + extracted_text + "\nSimplified Text:\n" + simplified_text
