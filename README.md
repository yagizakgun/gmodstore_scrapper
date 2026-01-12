# GModStore Job Market Discord Scraper

A Python application that automatically tracks job listings on GModStore and sends new listings to your Discord channel.

## 🌐 Language / Dil

- **[English](README.md)** (Current)
- **[Türkçe](docs/README_TR.md)**

---

## Features

- ✅ Automatic check every 30 minutes
- ✅ Only sends active listings (Apply, In Progress, Negotiations)
- ✅ Beautiful Discord embed messages
- ✅ Duplicate message prevention system
- ✅ Graceful shutdown (safe shutdown with Ctrl+C)
- ✅ Rate limit protection

## Installation

### 1. Requirements

- Python 3.8 or higher
- Windows PowerShell (for Windows) or Terminal (for Linux/Mac)

### 2. Project Setup

**Windows:**

```powershell
# Navigate to project directory
cd gmodstore_scrapper

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Linux/Mac:**

```bash
# Navigate to project directory
cd gmodstore_scrapper

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create Discord Webhook

1. Go to your Discord server and select the channel where you want to receive job listings
2. Click channel settings (⚙️)
3. **Integrations** → **Webhooks** → **New Webhook**
4. Give the webhook a name (e.g., "GModStore Jobs")
5. Click **Copy Webhook URL**

### 4. Configuration

Open `config.py` and paste your Discord webhook URL:

```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."
```

## Usage

### Starting

```powershell
# With virtual environment activated
python main.py
```

### Running in Background

**Windows:**

```powershell
# Start in background with PowerShell
Start-Process -NoNewWindow python -ArgumentList "main.py"
```

**Linux/Mac:**

```bash
# Start in background
nohup python main.py &
```

### Stopping

- Press **Ctrl+C** (graceful shutdown)
- Or close the console window

## Discord Embed Format

Each new listing is sent in the following format:

```
┌─────────────────────────────────────────────┐
│ [GModStore Logo]                            │
│                                             │
│ Looking for a Helix Gmod developer...       │
│ (Title - clickable link)                    │
│                                             │
│ 💰 Budget: $100.00                          │
│ 📁 Category: Gamemode                       │
│ 📊 Status: 🟢 Apply                         │
│ 📝 Applications: 2                          │
│ 👁️ Views: 47                                │
│ ⏰ Due Date: 2026-02-01                     │
│                                             │
│ Description:                                │
│ [Description text]                          │
│                                             │
│ Footer: GModStore Job Market                │
└─────────────────────────────────────────────┘
```

**Note:** This format is sent as a Discord embed message and appears visually formatted.

### Status Colors

- 🟢 **Apply** → Green
- 🟡 **In Progress** → Yellow
- 🟠 **Negotiations** → Orange
- ⚫ **Finished** → Gray (not sent)

## File Structure

```
gmodstore_scrapper/
├── main.py              # Main application
├── scraper.py           # GModStore scraper
├── discord_webhook.py   # Discord message sending
├── config.py            # Configuration
├── requirements.txt     # Python dependencies
├── seen_jobs.json       # Seen listings (auto-generated)
├── venv/                # Virtual environment (in gitignore)
├── README.md            # This file (English)
├── docs/                # Documentation folder
│   ├── README_TR.md         # Turkish version
│   ├── INSTALLATION.md      # Windows installation guide (English)
│   ├── KURULUM.md           # Windows installation guide (Turkish)
│   ├── LINUX_INSTALLATION.md # Linux installation guide (English)
│   └── LINUX_KURULUM.md     # Linux installation guide (Turkish)
├── scripts/             # Scripts folder
│   ├── start.bat            # Windows start script
│   └── setup_linux.sh       # Linux setup script
└── deploy/              # Deployment configurations
    ├── systemd/             # Systemd service files
    │   └── gmodstore-scraper.service
    └── docker/              # Docker deployment files
        ├── Dockerfile
        ├── docker-compose.yml
        └── README.md
```

## Configuration Options

You can modify the following in `config.py`:

| Setting | Default | Description |
|---------|---------|-------------|
| `CHECK_INTERVAL` | 1800 (30min) | Check interval (seconds) |
| `ACTIVE_JOB_STATUSES` | Apply, In Progress, Negotiations | Status types to send |
| `STATUS_COLORS` | ... | Discord embed colors |

## Troubleshooting

### "Webhook test failed" error

- Make sure the Discord webhook URL is correct
- Ensure the webhook hasn't been deleted
- Check your internet connection

### "No listings found" warning

- Check if GModStore is accessible
- HTML structure may have changed (scraper.py needs update)
- Run `scraper.py` in test mode: `python scraper.py`

### Virtual environment not activated

**Windows:**

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an error, change PowerShell execution policy:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

## Test Modes

### Scraper Test

```powershell
python scraper.py
```

### Discord Webhook Test

```powershell
python discord_webhook.py
```

## Updates

```powershell
# With virtual environment activated
pip install --upgrade -r requirements.txt
```

## Documentation

- **[Windows Installation Guide (English)](docs/INSTALLATION.md)**
- **[Windows Installation Guide (Turkish)](docs/KURULUM.md)**
- **[Linux Installation Guide (English)](docs/LINUX_INSTALLATION.md)**
- **[Linux Installation Guide (Turkish)](docs/LINUX_KURULUM.md)**

## License

MIT License

## Contact

You can use GitHub Issues for questions.

---

**Note:** This scraper respects GModStore's robots.txt rules and uses reasonable rate limiting. Please use responsibly.
