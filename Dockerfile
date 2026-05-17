# Use lightweight Python image
FROM python:3.11-slim

WORKDIR /app

# Install dependensi sistem untuk Pillow, OpenCV, dan LibreOffice (untuk PDF/Docs)
RUN apt-get update && apt-get install -y \
    libopenjp2-7 \
    libtiff6 \
    libgl1 \
    libglib2.0-0 \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pastikan folder temp_images selalu ada sebelum bot berjalan
RUN mkdir -p temp_images

CMD ["python", "converter.py"]
