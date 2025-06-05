"""
Service module for GCP storage operations and utility functions.
"""
from google.cloud import storage
import os
import datetime
import logging
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

def generate_timestamped_filename(filename: str) -> str:
    """
    Generates a filename with a timestamp appended before the extension.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    return f"{name}_{timestamp}{ext}" if ext else f"{filename}_{timestamp}"

def get_gcp_client(credentials_path: Optional[str] = None) -> storage.Client:
    """
    Initializes and returns a GCP storage client.
    """
    if credentials_path:
        return storage.Client.from_service_account_json(credentials_path)
    return storage.Client()  # Uses default credentials

def upload_to_bucket(client: storage.Client, bucket_name: str, blob_name: str, text: str) -> str:
    """
    Uploads text to a GCP bucket and returns the public URL.
    Raises ValueError if bucket_name or blob_name is missing.
    """
    if not bucket_name or not blob_name:
        logging.error("Bucket name and blob name must be provided.")
        raise ValueError("Bucket name and blob name must be provided.")
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(text, content_type="text/plain")
    logging.debug(f"Upload to GCP bucket complete: {bucket_name}/{blob_name}")
    return blob.public_url

def write_text_to_gcp_bucket(text: str, bucket_name: str, destination_blob_name: str, credentials_path: Optional[str] = None) -> str:
    """
    Writes the given text to a file in a GCP bucket and returns the public URL.
    Raises ValueError if required arguments are missing.
    """
    logging.debug(f"Preparing to upload text to GCP bucket: {bucket_name}, blob: {destination_blob_name}, credentials: {credentials_path}")
    if not text or not bucket_name or not destination_blob_name:
        logging.error("Text, bucket name, and destination blob name must be provided.")
        raise ValueError("Text, bucket name, and destination blob name must be provided.")
    destination_blob_name_with_timestamp = generate_timestamped_filename(destination_blob_name)
    client = get_gcp_client(credentials_path)
    return upload_to_bucket(client, bucket_name, destination_blob_name_with_timestamp, text) 