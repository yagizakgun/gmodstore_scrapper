# Deployment Configurations

This folder contains deployment configurations.

## Folder Structure

```
deploy/
├── systemd/              # Systemd service files (Linux)
│   └── gmodstore-scraper.service
└── docker/               # Docker deployment files
    ├── Dockerfile
    ├── docker-compose.yml
    └── README.md
```

## Systemd (Linux)

To run as a service on Linux servers using systemd:

```bash
# Copy service file
sudo cp deploy/systemd/gmodstore-scraper.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable gmodstore-scraper

# Start service
sudo systemctl start gmodstore-scraper
```

For detailed information: [docs/LINUX_INSTALLATION.md](../docs/LINUX_INSTALLATION.md)

## Docker

To run as a container using Docker:

```bash
# Using Docker Compose (recommended)
cd deploy/docker
docker-compose up -d

# Or manually
docker build -t gmodstore-scraper -f deploy/docker/Dockerfile .
docker run -d --name gmodstore-scraper --restart unless-stopped gmodstore-scraper
```

For detailed information: [deploy/docker/README.md](docker/README.md)

---

**[View Turkish Version](README_TR.md)**
