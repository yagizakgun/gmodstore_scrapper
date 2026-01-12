# Docker Deployment

Guide for running GModStore Scraper with Docker.

## Quick Start

### 1. Prepare Config File

Edit the `config.py` file in the project root directory and set your Discord webhook URL.

### 2. Build Docker Image

```bash
cd deploy/docker
docker build -t gmodstore-scraper -f Dockerfile ../..
```

Or from project root directory:

```bash
docker build -t gmodstore-scraper -f deploy/docker/Dockerfile .
```

### 3. Run Container

```bash
docker run -d \
  --name gmodstore-scraper \
  --restart unless-stopped \
  -v $(pwd)/config.py:/app/config.py:ro \
  -v $(pwd)/deploy/docker/data:/app/data \
  gmodstore-scraper
```

### Using Docker Compose (Recommended)

```bash
cd deploy/docker
docker-compose up -d
```

## Commands

### Stop Container

```bash
docker stop gmodstore-scraper
```

### Start Container

```bash
docker start gmodstore-scraper
```

### View Logs

```bash
docker logs -f gmodstore-scraper
```

### Remove Container

```bash
docker stop gmodstore-scraper
docker rm gmodstore-scraper
```

## Notes

- `config.py` file is mounted as read-only
- `seen_jobs.json` file is stored in `deploy/docker/data/` folder
- Container automatically restarts (restart policy: unless-stopped)

---

**[View Turkish Version](README_TR.md)**
