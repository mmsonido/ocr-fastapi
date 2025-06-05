"""
API endpoints for the OCR FastAPI application.
Includes the root endpoint serving index.html and the OCR extraction endpoint.
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse
import os
from app.services.ocr_service import extract_text_from_pdf
from app.services.gcp_storage_service import write_text_to_gcp_bucket
from pydantic import BaseModel
import logging
from typing import Optional

router = APIRouter()

def validate_pdf(file: UploadFile) -> None:
    """
    Validates that the uploaded file is a PDF.
    Raises HTTPException if not.
    """
    if file.content_type != "application/pdf":
        logging.warning("Uploaded file is not a PDF.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The file must be a PDF")

async def get_pdf_bytes(file: UploadFile) -> bytes:
    """
    Reads and returns the bytes of the uploaded file.
    """
    return await file.read()

def build_output_filename(filename: str) -> str:
    """
    Ensures the output filename ends with .txt
    """
    if not filename.endswith(".txt"):
        filename += ".txt"
    return filename

@router.get("/", response_class=HTMLResponse)
async def root() -> str:
    """
    Serves the index.html file at the root endpoint ('/').
    """
    path = os.path.join("static", "index.html")
    with open(path, "r") as f:
        return f.read()

class ExtractTextResponse(BaseModel):
    text: str

@router.post("/extract-text", response_model=ExtractTextResponse, status_code=status.HTTP_200_OK)
async def extract_text(file: UploadFile = File(...)) -> ExtractTextResponse:
    """
    Extracts text from an uploaded PDF file using OCR.
    Returns the extracted text as JSON.
    """
    validate_pdf(file)
    pdf_bytes = await get_pdf_bytes(file)
    try:
        text = extract_text_from_pdf(pdf_bytes)
    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error processing PDF: {e}")
    return ExtractTextResponse(text=text)

class ExtractTextToBucketResponse(BaseModel):
    url: str

@router.post("/extract-text-to-bucket", response_model=ExtractTextToBucketResponse, status_code=status.HTTP_200_OK)
async def extract_text_to_bucket(
    file: UploadFile = File(...),
    filename: Optional[str] = None
) -> ExtractTextToBucketResponse:
    """
    Extracts text from an uploaded PDF file using OCR and writes it to a GCP bucket.
    Returns the public URL of the uploaded text file.
    """
    validate_pdf(file)
    pdf_bytes = await get_pdf_bytes(file)
    try:
        text = extract_text_from_pdf(pdf_bytes)
        logging.debug(f"Extracted text length: {len(text)}")
        bucket_name = os.getenv("GCP_BUCKET_NAME")
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not bucket_name:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="GCP_BUCKET_NAME environment variable not set")
        # Use provided filename or default
        if not filename:
            filename = file.filename 
        filename = build_output_filename(filename)
        logging.debug(f"Preparing to upload to bucket: {bucket_name}, filename: {filename}, credentials: {credentials_path}")
        url = write_text_to_gcp_bucket(text, bucket_name, filename, credentials_path)
        logging.debug(f"Upload complete. File URL: {url}")
    except Exception as e:
        logging.error(f"Error processing PDF or uploading to bucket: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")
    return ExtractTextToBucketResponse(url=url) 