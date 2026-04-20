import pytesseract
import re
import os
from PIL import Image

if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Exact format: XXXX-XXXXXX-XXXX (4-6-4 alphanumeric)
CODE_PATTERN = re.compile(r'\b([A-Z0-9]{4}-[A-Z0-9]{6}-[A-Z0-9]{4})\b')

# Handle OCR spacing errors: XXXX XXXXXX XXXX
SPACED_PATTERN = re.compile(r'\b([A-Z0-9]{4})\s([A-Z0-9]{6})\s([A-Z0-9]{4})\b')


def preprocess_frame(image_path):
    """Convert to grayscale to improve OCR accuracy"""
    img = Image.open(image_path).convert("L")
    return img


def extract_codes_from_frame(image_path):
    img = preprocess_frame(image_path)
    config = "--psm 11 --oem 3"
    text = pytesseract.image_to_string(img, config=config).upper()

    codes = set()
    codes.update(CODE_PATTERN.findall(text))
    for a, b, c in SPACED_PATTERN.findall(text):
        codes.add(f"{a}-{b}-{c}")

    return codes


def scan_all_frames(frame_paths):
    all_codes = set()
    for path in frame_paths:
        codes = extract_codes_from_frame(path)
        if codes:
            print(f"   FOUND in {os.path.basename(path)}: {codes}")
            all_codes.update(codes)
        os.remove(path)
    return list(all_codes)
