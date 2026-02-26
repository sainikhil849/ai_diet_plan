import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Working directory: {os.getcwd()}")

print("-" * 50)
print("Checking EasyOCR...")
try:
    import easyocr
    print("EasyOCR imported successfully.")
    try:
        print("Attempting to initialize EasyOCR Reader (this might download models)...")
        reader = easyocr.Reader(['en'])
        print("EasyOCR Reader initialized successfully.")
    except Exception as e:
        print(f"EasyOCR initialization failed: {e}")
except ImportError as e:
    print(f"EasyOCR import failed: {e}")

print("-" * 50)
print("Checking Pytesseract...")
try:
    import pytesseract
    print("Pytesseract imported successfully.")
    try:
        from PIL import Image
        import numpy as np
        # Create a dummy image
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        text = pytesseract.image_to_string(img)
        print("Pytesseract execution successful (even if text is empty).")
    except Exception as e:
        print(f"Pytesseract execution failed: {e}")
except ImportError as e:
    print(f"Pytesseract import failed: {e}")
