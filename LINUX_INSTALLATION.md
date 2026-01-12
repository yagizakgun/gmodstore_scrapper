# 🐧 Linux Installation and Continuous Running Guide

This guide helps you install and keep the GModStore Job Scraper bot running 24/7 on your Linux server.

---

## 📋 Requirements

- Ubuntu 20.04+ / Debian 10+ / CentOS 8+ or any modern Linux distribution
- Python 3.8+
- Internet access
- sudo privileges

---

## 🚀 Quick Installation

### 1. Upload Files to Server

Copy files to your server (example: `/home/user/gmodstore_scrapper`):

```bash
# Clone with Git (recommended)
cd ~
git clone https://github.com/username/gmodstore_scrapper.git

# Or copy with SCP (from Windows)
# scp -r gmodstore_scrapper user@server_ip:/home/user/
```

### 2. Install Python and Dependencies

```bash
# Install Python and pip (if not installed)
sudo apt update
sudo apt install python3 python3-pip python3-venv -y

# Navigate to project directory
cd ~/gmodstore_scrapper

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Settings

```bash
# Edit config.py file
nano config.py
```

Set your Discord Webhook URL and save (Ctrl+X, Y, Enter).

### 4. Manual Test (Optional)

```bash
# Test the bot
source venv/bin/activate
python main.py
```

Press Ctrl+C to stop.

---

## 🔄 Automatic Running with Systemd (Recommended)

Systemd will:
- ✅ Automatically start bot when server boots
- ✅ Automatically restart if it crashes
- ✅ Keep logs organized

### 1. Edit Service File

```bash
# Edit service file
nano ~/gmodstore_scrapper/gmodstore-scraper.service
```

**Replace the following lines with your information:**

```ini
User=YOUR_USERNAME          → User=your_username
Group=YOUR_USERNAME         → Group=your_username
WorkingDirectory=/home/YOUR_USERNAME/gmodstore_scrapper → WorkingDirectory=/home/your_username/gmodstore_scrapper
ExecStart=/home/YOUR_USERNAME/gmodstore_scrapper/venv/bin/python main.py → ExecStart=/home/your_username/gmodstore_scrapper/venv/bin/python main.py
```

### 2. Install Service to System

```bash
# Copy service file
sudo cp ~/gmodstore_scrapper/gmodstore-scraper.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable gmodstore-scraper

# Start service
sudo systemctl start gmodstore-scraper
```

### 3. Check Status

```bash
# View service status
sudo systemctl status gmodstore-scraper

Output should look like:

```
● gmodstore-scraper.service - GModStore Job Market Discord Scraper
     Active: active (running) since ...
```

---

## 📊 Useful Commands

### Service Management

```bash
# Check status
sudo systemctl status gmodstore-scraper

# Start
sudo systemctl start gmodstore-scraper

# Stop
sudo systemctl stop gmodstore-scraper

# Restart
sudo systemctl restart gmodstore-scraper

# Disable auto-start on boot
sudo systemctl disable gmodstore-scraper
```

### View Logs

```bash
# View recent logs
sudo journalctl -u gmodstore-scraper -n 50

# Live log follow
sudo journalctl -u gmodstore-scraper -f

# Today's logs
sudo journalctl -u gmodstore-scraper --since today

# Last 1 hour's logs
sudo journalctl -u gmodstore-scraper --since "1 hour ago"
```

---

## 🔧 Troubleshooting

### "Permission denied" Error

```bash
# Fix file permissions
chmod +x ~/gmodstore_scrapper/main.py
chmod 755 ~/gmodstore_scrapper
```

### Service Won't Start

```bash
# View detailed error message
sudo journalctl -u gmodstore-scraper -n 100 --no-pager

# Test by running manually
cd ~/gmodstore_scrapper
source venv/bin/activate
python main.py
```

### Python Not Found

```bash
# Check Python path
which python3

# Update ExecStart in service file with full path
# Example: ExecStart=/usr/bin/python3 main.py
```

### Webhook Error

```bash
# Check config.py
cat ~/gmodstore_scrapper/config.py | grep WEBHOOK

# Make sure URL is correct
```

---

## 🔄 Updating

```bash
# Stop service
sudo systemctl stop gmodstore-scraper

# Make updates (change files or git pull)
cd ~/gmodstore_scrapper
# ... changes ...

# Update dependencies (if needed)
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start gmodstore-scraper
```

---

## 🐳 Alternative: Running with Docker (Optional)

If you want to use Docker:

```bash
# Install Docker
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker

# Build Dockerfile (already in project)
cd ~/gmodstore_scrapper
docker build -t gmodstore-scraper .

# Run
docker run -d --name gmodstore-scraper --restart=always gmodstore-scraper
```

---

## 📝 Notes

1. **Security**: The webhook URL in your `config.py` is sensitive information. Restrict file permissions:
   ```bash
   chmod 600 ~/gmodstore_scrapper/config.py
   ```

2. **Performance**: Bot uses very few resources (~20-50MB RAM).

3. **Time Zone**: Set your server's time zone:
   ```bash
   sudo timedatectl set-timezone Europe/Istanbul
   ```

4. **Firewall**: Allow outgoing HTTPS connections (port 443) - usually open by default.

---

## ❓ Frequently Asked Questions

**Q: How much RAM does the bot use?**
A: Approximately 20-50MB RAM.

**Q: What happens if the server shuts down?**
A: Systemd will automatically start the bot when the server boots.

**Q: What if the bot crashes?**
A: Systemd will automatically restart it after 10 seconds.

**Q: Do logs fill up the disk?**
A: No, journald automatically rotates logs.

---

**Happy using! 🚀**

---

**[View Turkish Version](LINUX_KURULUM.md)**
