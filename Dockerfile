FROM python:3.11-slim

# Parent working directory
WORKDIR /usr/src/app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app folder contents directly into WORKDIR
COPY app/ .

# Expose port
ENV PORT=8080

# Start uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port=8080"]
