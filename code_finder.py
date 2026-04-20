import pytesseract
import re
import os
from PIL import Image

_win_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(_win_tesseract):
    pytesseract.pytesseract.tesseract_cmd = _win_tesseract

# Exact format: XXXX-XXXXXX-XXXX (4-6-4 alphanumeric)
CODE_PATTERN = re.compile(r'\b([A-Z0-9]{4}-[A-Z0-9]{6}-[A-Z0-9]{4})\b')

# Handle OCR spacing errors: XXXX XXXXXX XXXX
SPACED_PATTERN = re.compile(r'\b([A-Z0-9]{4})\s([A-Z0-9]{6})\s([A-Z0-9]{4})\b')


def preprocess_frame(image_path):
    """Convert to grayscale to improve OCR accuracy"""
    img = Image.open(image_path).convert("L")
    return img


def is_real_code(code):
    parts = code.replace("-", "")
    has_letter = any(c.isalpha() for c in parts)
    has_digit = any(c.isdigit() for c in parts)
    return has_letter and has_digit


def extract_codes_from_frame(image_path):
    img = preprocess_frame(image_path)
    config = "--psm 11 --oem 3"
    text = pytesseract.image_to_string(img, config=config).upper()

    codes = set()
    for code in CODE_PATTERN.findall(text):
        if is_real_code(code):
            codes.add(code)
    for a, b, c in SPACED_PATTERN.findall(text):
        code = f"{a}-{b}-{c}"
        if is_real_code(code):
            codes.add(code)

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
