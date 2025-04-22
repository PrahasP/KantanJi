import requests
import ocr  # Assuming the OCR module you already have is imported

def get_jisho_meaning(word):
    """
    Fetches the meaning and reading of a Japanese word from Jisho.org.
    
    Args:
    - word (str): The Japanese word to be translated.
    
    Returns:
    - dict: The meaning and reading information from Jisho.org, or None if not found.
    """
    # Jisho.org API endpoint
    url = f"https://jisho.org/api/v1/search/words?keyword={word}"
    
    # Send the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Check if any words were found
        if data["data"]:
            # Extract the first result's meanings and readings
            word_data = data["data"][0]
            meanings = word_data.get("senses", [{}])[0].get("english_definitions", ["No meaning found"])
            readings = word_data.get("japanese", [{}])[0].get("reading", "No reading found")
            
            return {
                "word": word,
                "meanings": meanings,
                "readings": readings
            }
    return None

def translate_text_with_jisho(text):
    """
    Translates the given text using Jisho.org API (one word at a time).
    
    Args:
    - text (str): The text to be translated.
    
    Returns:
    - str: The translated text with meanings and readings for each word.
    """
    # Split the text into words (simple split by space for now, could be improved)
    words = text.split()
    translated_text = ""

    for word in words:
        result = get_jisho_meaning(word)
        
        if result:
            translated_text += f"Original: {result['word']}\n"
            translated_text += f"Reading: {result['readings']}\n"
            translated_text += f"Meanings: {', '.join(result['meanings'])}\n"
            translated_text += "-" * 40 + "\n"
        else:
            translated_text += f"Original: {word} (No translation found)\n"
            translated_text += "-" * 40 + "\n"

    return translated_text

def display_original_vs_translated(text):
    """
    Display the original and translated text side by side using Jisho.org.
    
    Args:
    - text (str): The text to be translated.
    """
    translated_text = translate_text_with_jisho(text)
    
    # Display original and translated text
    print("Original Text:")
    print(text)
    print("\nTranslated Text:")
    print(translated_text)

if __name__ == "__main__":
    # Example usage: get the text from OCR (assuming OCR processing is done)
    detected_text = ocr.read_text_from_image("captured_snip.png")  # Replace with actual file path
    
    # Now translate and display original vs translated
    display_original_vs_translated(detected_text)  # This will display the original text and translations
