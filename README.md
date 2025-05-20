# OCR Image Text Extractor

A web application that allows users to upload images and extract text using OCR (Optical Character Recognition) technology.

## Features

- Upload images via drag-and-drop or file selection
- Extract text from various image formats (PNG, JPG, JPEG, GIF, BMP, TIFF)
- Image preprocessing to improve OCR accuracy
- Copy extracted text to clipboard

## Requirements

- Python 3.6+
- Tesseract OCR engine
- Flask web framework
- OpenCV for image processing
- pytesseract for OCR functionality

## Installation

1. Install Tesseract OCR:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure Tesseract path (if needed):
   - Open `ocr_processor.py`
   - Uncomment and modify the line: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Upload an image using the interface and view the extracted text.

## Project Structure

- `app.py`: Main Flask application
- `ocr_processor.py`: OCR processing functions
- `templates/index.html`: Web interface
- `uploads/`: Directory for storing uploaded images

## License

MIT