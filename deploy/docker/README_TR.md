# Docker Deployment

Docker ile GModStore Scraper'ı çalıştırma rehberi.

## Hızlı Başlangıç

### 1. Config Dosyasını Hazırlayın

Proje root dizinindeki `config.py` dosyasını düzenleyin ve Discord webhook URL'nizi ayarlayın.

### 2. Docker Image Oluşturun

```bash
cd deploy/docker
docker build -t gmodstore-scraper -f Dockerfile ../..
```

Veya proje root dizininden:

```bash
docker build -t gmodstore-scraper -f deploy/docker/Dockerfile .
```

### 3. Container'ı Çalıştırın

```bash
docker run -d \
  --name gmodstore-scraper \
  --restart unless-stopped \
  -v $(pwd)/config.py:/app/config.py:ro \
  -v $(pwd)/deploy/docker/data:/app/data \
  gmodstore-scraper
```

### Docker Compose ile (Önerilen)

```bash
cd deploy/docker
docker-compose up -d
```

## Komutlar

### Container'ı Durdurma

```bash
docker stop gmodstore-scraper
```

### Container'ı Başlatma

```bash
docker start gmodstore-scraper
```

### Logları Görüntüleme

```bash
docker logs -f gmodstore-scraper
```

### Container'ı Silme

```bash
docker stop gmodstore-scraper
docker rm gmodstore-scraper
```

## Notlar

- `config.py` dosyası read-only olarak mount edilir
- `seen_jobs.json` dosyası `deploy/docker/data/` klasöründe saklanır
- Container otomatik olarak yeniden başlatılır (restart policy: unless-stopped)

---

**[View English Version](README.md)**
