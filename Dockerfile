# Use an official Python base image (slim to minimize size)
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install required system dependencies (Tesseract and Poppler)
RUN apt-get update && apt-get install -y \
    tesseract-ocr poppler-utils && \
    apt-get clean

# Copy requirements and install them (no cache to reduce layer size)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code (assuming structure as above)
COPY app/ app/
COPY static/ static/

# Specify the port the app will listen on (Cloud Run uses 8080 by default)
ENV PORT=8080
EXPOSE 8080

# Default command to launch the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]