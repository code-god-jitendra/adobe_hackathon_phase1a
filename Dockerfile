# 1. Base image
FROM python:3.11-slim

# 2. Create app directory
WORKDIR /app

# 3. Install system deps (if any)
#    none needed beyond pip in slim

# 4. Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your model and code
COPY model/heading_model.pkl model/heading_model.pkl
COPY outline_extractor.py utils.py ./

# 6. Entrypoint
ENTRYPOINT ["python", "outline_extractor.py"]
