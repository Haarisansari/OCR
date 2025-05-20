import cv2
import pytesseract
import os

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

def process_image(image_path):
    """
    Process an image and extract text using OCR
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        str: Extracted text from the image
    """
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        # Preprocess the image
        processed_image = preprocess_image(image_path)
        
        # Apply OCR to extract text
        extracted_text = pytesseract.image_to_string(processed_image)
        
        return extracted_text
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
    text = process_image(image_path)
    return {"raw_text": text}