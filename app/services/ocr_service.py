"""
Service module for OCR operations on PDF files.
"""
from pdf2image import convert_from_bytes
import pytesseract
import logging
from typing import List
from concurrent.futures import ProcessPoolExecutor


def pdf_to_images(pdf_bytes: bytes) -> List:
    """
    Converts PDF bytes to a list of images.
    Raises ValueError if pdf_bytes is empty.
    """
    if not pdf_bytes:
        logging.error("No PDF bytes provided for conversion.")
        raise ValueError("No PDF bytes provided.")
    return convert_from_bytes(pdf_bytes)

def image_to_text(img) -> str:
    """
    Extracts text from a single image using pytesseract.
    """
    return pytesseract.image_to_string(img, lang="eng")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Converts a PDF (as bytes) to images and extracts text from each page using pytesseract OCR in parallel.
    Raises RuntimeError if OCR processing fails.
    """
    try:
        images = pdf_to_images(pdf_bytes)
        with ProcessPoolExecutor() as executor:
            texts = list(executor.map(image_to_text, images))
        return ''.join(texts)
    except Exception as e:
        logging.error(f"OCR extraction failed: {e}")
        raise RuntimeError(f"OCR extraction failed: {e}")