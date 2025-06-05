# OCR PDF to TXT Converter (FastAPI + Cloud Ready)

## Overview

This project implements a robust backend and simple frontend for extracting text from PDF files using OCR (Optical Character Recognition). The backend is designed for scalability and cloud deployment, and the frontend allows users to upload PDF files and receive extracted text or upload the result to Google Cloud Storage.

**Key Features:**
- Extracts text from PDF files using Tesseract OCR.
- Supports uploading the extracted text to a Google Cloud Storage bucket.
- Simple, modern frontend for user interaction.
- Cloud-native: ready for deployment on Google Cloud Run.
- Easily extensible for future features.

---

## Table of Contents

- [Architecture](#architecture)
- [Cloud Infrastructure Diagram](#cloud-infrastructure-diagram)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
- [Frontend Usage](#frontend-usage)
- [API Endpoints](#api-endpoints)
- [Testing with Example PDFs](#testing-with-example-pdfs)
- [Extending the Project](#extending-the-project)
- [License](#license)

---

## Architecture

- **Backend:** FastAPI app with endpoints for PDF upload, OCR extraction, and GCP bucket upload.
- **OCR Engine:** Uses `pdf2image` to convert PDF pages to images, then `pytesseract` for text extraction.
- **Cloud Storage:** Optionally uploads extracted text to a Google Cloud Storage bucket.
- **Frontend:** Single-page HTML/JS app for uploading PDFs and displaying results.

---

## Cloud Infrastructure Diagram

```
[User]
   |
   v
[Frontend (Static HTML/JS)]
   |
   v
[FastAPI Backend (Cloud Run)]
   |
   +-------------------+
   |                   |
   v                   v
[OCR Engine]     [Google Cloud Storage Bucket]
```

**Recommended Cloud Setup:**
- **Google Cloud Run:** Hosts the FastAPI backend as a containerized service.
- **Google Cloud Storage:** Stores extracted TXT files for public or private access.
- **(Optional) Google Artifact Registry:** For storing Docker images.
- **IAM Service Account:** For secure access to GCP resources.

---

## Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **OCR:** Tesseract OCR (`pytesseract`), `pdf2image`, `Pillow`
- **Cloud:** Google Cloud Storage, Google Cloud Run
- **Frontend:** HTML, CSS, JavaScript (no frameworks)
- **Containerization:** Docker

---

## Setup & Installation

### Prerequisites

- Python 3.8+
- [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) (must be installed and in your PATH)
- [Poppler](http://blog.alivate.com.au/poppler-windows/) (for `pdf2image`)
- Google Cloud account (for cloud deployment and storage)
- Docker (for containerization and deployment)
- (Optional) `gcloud` CLI for deployment

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Copy `env_example` to `.env` and fill in your values:

```bash
cp env_example .env
```

**Variables:**

| Name                        | Description                                      |
|-----------------------------|--------------------------------------------------|
| `DOCKER_IMAGE`              | Docker image name for deployment                 |
| `SERVICE_NAME`              | Name of the Cloud Run service                    |
| `REGION`                    | GCP region for deployment                        |
| `GCP_BUCKET_NAME`           | Name of your GCP storage bucket                  |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to your GCP service account JSON key |

Example `.env`:
```
DOCKER_IMAGE=gcr.io/your-project/ocr-fastapi:latest
SERVICE_NAME=ocr-fastapi-service
REGION=us-central1
GCP_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS=keys/your-service-account.json
```

---

## Creating Google Cloud Service Account Keys

To enable the backend to upload files to your Google Cloud Storage bucket, you need a service account key with the appropriate permissions:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **IAM & Admin > Service Accounts**.
3. Click **Create Service Account**.
   - Give it a name (e.g., `ocr-fastapi-service-account`).
   - Click **Create and Continue**.
4. Assign the role **Storage Object Admin** (or a more restrictive role if desired).
   - Click **Continue** and then **Done**.
5. In the list, click your new service account, then go to the **Keys** tab.
6. Click **Add Key > Create new key**.
   - Select **JSON** and click **Create**.
   - Download the JSON file and place it in your project (e.g., in the `keys/` directory).
7. Set the `GOOGLE_APPLICATION_CREDENTIALS` variable in your `.env` file to the path of this JSON file (e.g., `keys/your-service-account.json`).

**Important:** Never commit your service account key to version control. The `.gitignore` is already configured to protect files in the `keys/` directory.

---

## Running Locally

1. **Install Tesseract and Poppler**

   - **macOS:**  
     ```bash
     brew install tesseract poppler
     ```
   - **Ubuntu:**  
     ```bash
     sudo apt-get install tesseract-ocr poppler-utils
     ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your `.env` file** (see above).

4. **Run the FastAPI app**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the frontend:**  
   Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Frontend Usage

- Click "Choose PDF file" and select a PDF.
- Select one or both actions:
  - **Print:** Extracts and displays the text in the browser.
  - **Upload to bucket:** Extracts text and uploads it as a `.txt` file to your configured GCP bucket.
- Click "Process" to run OCR and see results or get a public link to the uploaded file.

---

## API Endpoints

| Method | Endpoint                  | Description                                      |
|--------|---------------------------|--------------------------------------------------|
| POST   | `/extract-text`           | Upload a PDF, returns extracted text as JSON     |
| POST   | `/extract-text-to-bucket` | Upload a PDF, returns public URL of TXT in GCP   |

**Example request:**

```bash
curl -F "file=@your.pdf" http://localhost:8000/extract-text
```

---

## Testing with Example PDFs

- Use the two provided PDF files (see assignment) to test both frontend and backend.
- The frontend allows you to upload and process these files directly.
- For API testing, use `curl` or Postman as shown above.

---

## Extending the Project

- The backend is modular: add new endpoints or services easily.
- Add authentication, support for more file types, or advanced OCR options as needed.
- The cloud setup is ready for scaling and integration with other GCP services.
- Add CI/CD integration
