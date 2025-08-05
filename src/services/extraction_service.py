import logging
import traceback
from io import BytesIO

import fitz  # PyMuPDF
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import cv2
import numpy as np


def preprocess_image(img: Image.Image) -> Image.Image:
    """Convert image to grayscale and apply binary thresholding for better OCR."""
    open_cv_image = np.array(img.convert('L'))  # Convert to grayscale
    _, thresh = cv2.threshold(open_cv_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(thresh)


def extract_text_from_pdf(file_bytes: bytes, task_log: dict = None) -> str:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if task_log is None:
        task_log = {}

    text = ""

    # First attempt: extract text directly (good for system-generated PDFs)
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            text = ''.join(page.get_text() for page in doc)
        if text.strip():
            task_log["text_extraction_method"] = "fitz"
            return text
    except Exception as e:
        err = f"Failed to open PDF with PyMuPDF: {e}"
        logging.error(err)
        traceback.print_exc()
        task_log["fitz_error"] = err

    # Second attempt: OCR via pdf2image + pytesseract (good for scanned or handwritten PDFs)
    try:
        images = convert_from_bytes(file_bytes, poppler_path="C:/poppler/Library/bin")
        ocr_text = ""
        for idx, img in enumerate(images):
            processed_img = preprocess_image(img)
            ocr_result = pytesseract.image_to_string(processed_img, lang='eng', config='--psm 6')
            ocr_text += ocr_result
            task_log[f"ocr_page_{idx+1}"] = ocr_result[:100]  # Preview of each page
        if ocr_text.strip():
            task_log["text_extraction_method"] = "ocr"
            return ocr_text
    except Exception as e:
        err = f"OCR extraction failed: {e}"
        logging.error(err)
        traceback.print_exc()
        task_log["ocr_error"] = err

    task_log["text_extraction_method"] = "none"
    return ""
