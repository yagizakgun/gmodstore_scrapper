# Quick Installation Guide

## 1. Get Discord Webhook URL

1. Select a channel in your Discord server (e.g., #gmodstore-jobs)
2. Go to channel settings (⚙️ icon)
3. **Integrations** → **Webhooks**
4. Click **New Webhook** button
5. Give the webhook a name: "GModStore Jobs"
6. Click **Copy Webhook URL** button

## 2. Configure Webhook URL

Open `config.py` file with a text editor and find this line:

```python
DISCORD_WEBHOOK_URL = "BURAYA_WEBHOOK_URL_GIRILECEK"
```

Paste your copied webhook URL between the quotation marks:

```python
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1234567890/abcdefghijklmnopqrstuvwxyz"
```

Save and close the file.

## 3. Start the Application

### Method 1: Using Batch File (Recommended)

Double-click the `scripts/start.bat` file. The application will start automatically.

### Method 2: Using PowerShell

```powershell
# Navigate to project folder
cd gmodstore_scrapper

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start the application
python main.py
```

## 4. Check if Application is Running

When the application starts successfully:

1. You will see "🚀 GModStore Job Scraper Başlatıldı" message in your Discord channel
2. You will see these messages in the console output:

```powershell
================================================
GModStore Job Market Discord Scraper
================================================
[SUCCESS] Webhook test başarılı!
[INFO] Bot başlatıldı. Ctrl+C ile durdurun.
```

## 5. How It Works

- The application checks GModStore **every 30 minutes**
- Sends new job listings to Discord when found
- Does not send the same listing multiple times (tracks with seen_jobs.json)
- Only sends **active listings** (Apply, In Progress, Negotiations)
- Listings with "Finished" status are not sent

## 6. Stop the Application

- Press **Ctrl+C**
- Or close the console window

The application saves the list of seen listings when closing, so it won't send the same listings again when you restart it.

## 7. Change Settings

You can modify the following in `config.py`:

### Change Check Interval

```python
CHECK_INTERVAL = 1800  # 30 minutes (in seconds)
```

Example values:
- 5 minutes: `300`
- 15 minutes: `900`
- 30 minutes: `1800`
- 1 hour: `3600`

### Change Job Statuses to Send

```python
ACTIVE_JOB_STATUSES = ["Apply", "In Progress", "Negotiations"]
```

To send only new listings:

```python
ACTIVE_JOB_STATUSES = ["Apply"]
```

### Change Discord Embed Colors

```python
STATUS_COLORS = {
    "Apply": 0x00FF00,        # Green
    "In Progress": 0xFFFF00,  # Yellow
    "Negotiations": 0xFFA500, # Orange
    "Finished": 0x808080      # Gray
}
```

Color codes are in hex format (6-digit code starting with 0x).

## 8. Troubleshooting

### "PowerShell execution policy" error

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "DISCORD_WEBHOOK_URL not set" error

Make sure you've correctly set the webhook URL in `config.py`.

### "Webhook test failed" error

- Check if the webhook URL is correct
- Check your internet connection
- Check if the webhook hasn't been deleted in Discord

### No listings are coming

1. Manually check if there are new listings on GModStore
2. Run `scraper.py` in test mode:
   ```powershell
   python scraper.py
   ```
3. HTML structure may have changed, scraper update may be needed

## 9. Auto-Start (Windows Startup)

To run automatically on Windows startup:

1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Copy a shortcut of `start.bat` to this folder

Or use Task Scheduler for more advanced settings.

## Support

If you encounter any issues, check the console output while `main.py` is running.
Error messages start with `[ERROR]` tag.

---

**[View Turkish Version](KURULUM.md)** | **[View Main README](../README.md)**
