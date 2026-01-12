# Deployment Configurations

Bu klasör deployment (dağıtım) konfigürasyonlarını içerir.

## Klasör Yapısı

```
deploy/
├── systemd/              # Systemd service dosyaları (Linux)
│   └── gmodstore-scraper.service
└── docker/               # Docker deployment dosyaları
    ├── Dockerfile
    ├── docker-compose.yml
    └── README.md
```

## Systemd (Linux)

Linux sunucularda systemd ile servis olarak çalıştırmak için:

```bash
# Service dosyasını kopyala
sudo cp deploy/systemd/gmodstore-scraper.service /etc/systemd/system/

# Systemd'yi yeniden yükle
sudo systemctl daemon-reload

# Servisi etkinleştir (açılışta başlat)
sudo systemctl enable gmodstore-scraper

# Servisi başlat
sudo systemctl start gmodstore-scraper
```

Detaylı bilgi için: [docs/LINUX_KURULUM.md](../docs/LINUX_KURULUM.md)

## Docker

Docker ile container olarak çalıştırmak için:

```bash
# Docker Compose ile (önerilen)
cd deploy/docker
docker-compose up -d

# Veya manuel olarak
docker build -t gmodstore-scraper -f deploy/docker/Dockerfile .
docker run -d --name gmodstore-scraper --restart unless-stopped gmodstore-scraper
```

Detaylı bilgi için: [deploy/docker/README.md](docker/README.md)

---

**[View English Version](README.md)**
