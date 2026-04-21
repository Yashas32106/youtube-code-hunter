import re
import os
import numpy as np
import easyocr

_reader = None

def _get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    return _reader

# Exact format: XXXX-XXXXXX-XXXX (4-6-4 alphanumeric)
CODE_PATTERN = re.compile(r'([A-Z0-9]{4}-[A-Z0-9]{6}-[A-Z0-9]{4})')

# Handle OCR spacing errors: XXXX XXXXXX XXXX
SPACED_PATTERN = re.compile(r'([A-Z0-9]{4})\s([A-Z0-9]{6})\s([A-Z0-9]{4})')


def extract_codes_from_frame(image_path):
    reader = _get_reader()
    # Read top 25% of frame — codes appear at top, subtitles at bottom
    import cv2
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    top = img[0:int(h * 0.25), :]

    results = reader.readtext(top, detail=0)
    text = " ".join(results).upper()

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
