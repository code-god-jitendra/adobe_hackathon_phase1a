# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY outline_extractor.py .
COPY utils.py .
COPY extract_candidates.py .
COPY model/ model/
COPY input/ input/

# Create output folder
RUN mkdir -p /app/output

# Run the outline extractor
CMD ["python", "outline_extractor.py"]
