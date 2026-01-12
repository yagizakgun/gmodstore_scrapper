# GModStore Job Scraper Docker Image
FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY *.py ./

# Zaman dilimi (opsiyonel)
ENV TZ=Europe/Istanbul

# Unbuffered output
ENV PYTHONUNBUFFERED=1

# Çalıştır
CMD ["python", "main.py"]
