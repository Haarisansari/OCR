import cv2
import pytesseract
import os
import requests
import json

# Set the path to tesseract executable
# Uncomment and modify the line below if tesseract is not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        numpy.ndarray: Preprocessed image
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to handle shadows and normalize the image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Apply noise reduction
    denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
    
    return denoised

def translate_text(text, target_lang='en'):
    """
    Translate text using Google Translate web API
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code
        
    Returns:
        dict: Translation result with detected language and translated text
    """
    import urllib.parse
    import urllib.request
    import json
    
    try:
        # URL encode the text
        text_encoded = urllib.parse.quote(text)
        
        # Create Google Translate URL
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={text_encoded}"
        
        # Create a request with a user-agent to avoid being blocked
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        # Get the response
        response = urllib.request.urlopen(req)
        
        # Parse the JSON response
        result = json.loads(response.read().decode('utf-8'))
        
        # Extract the translated text
        translated_text = ''.join([sentence[0] for sentence in result[0]])
        
        # Extract detected language
        detected_lang = result[2] if len(result) > 2 else "unknown"
        
        return {
            "detected_language": detected_lang,
            "translated_text": translated_text,
            "success": True
        }
    except Exception as e:
        # Fallback to original text if translation fails
        return {
            "detected_language": "unknown",
            "translated_text": None,
            "success": False,
            "error": str(e)
        }


def process_image(image_path, translate_to_english=False):
    """
    Process an image and extract text using OCR
    
    Args:
        image_path (str): Path to the input image
        translate_to_english (bool): Whether to translate non-English text to English
        
    Returns:
        dict: Dictionary containing extracted text and translation information
    """
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)
        
        # Use Indian languages + English
        # The '+' tells Tesseract to use multiple language models
        extracted_text = pytesseract.image_to_string(
            processed_image, 
            lang='eng+hin+tam+tel+mar+pan+guj+ben'
        )
        
        result = {
            "original_text": extracted_text,
            "language": "auto",  # We're using multiple languages
            "translated_text": None,
            "is_translated": False
        }
        
        # If translation is requested and text was extracted
        if translate_to_english and extracted_text.strip():
            try:
                # Use LibreTranslate API instead of googletrans
                translation = translate_text(extracted_text)
                
                if translation["success"]:
                    result["language"] = translation["detected_language"]
                    
                    # Only set as translated if language is not English
                    if translation["detected_language"] != "en":
                        result["translated_text"] = translation["translated_text"]
                        result["is_translated"] = True
            except Exception as e:
                # If translation fails, return the original text
                result["translation_error"] = str(e)
        
        return result
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

def extract_structured_data(image_path):
    """
    Extract structured data from specific types of documents
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        dict: Structured data extracted from the image
    """
    # This is a placeholder for more advanced OCR functionality
    # For example, extracting specific fields from forms, invoices, etc.
    
    # For now, we'll just return the raw text as a dictionary
    result = process_image(image_path)
    return {"raw_text": result["original_text"]}
