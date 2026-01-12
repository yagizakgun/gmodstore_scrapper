# GModStore Job Scraper Configuration

# Discord Webhook URL - PASTE YOUR WEBHOOK URL HERE
DISCORD_WEBHOOK_URL = "DISCORD_WEBHHOK_URL"

# Check interval (in seconds)
CHECK_INTERVAL = 1800  # 30 minutes

# GModStore job listings URL
GMODSTORE_JOBS_URL = "https://www.gmodstore.com/jobmarket/jobs/browse"

# User-Agent (to prevent bot detection)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Active job statuses (only these will be sent)
ACTIVE_JOB_STATUSES = ["Apply", "In Progress", "Negotiations"]

# Discord embed colors (by status)
STATUS_COLORS = {
    "Apply": 0x00FF00,        # Green
    "In Progress": 0xFFFF00,  # Yellow
    "Negotiations": 0xFFA500, # Orange
    "Finished": 0x808080      # Gray
}

# GModStore logo URL
GMODSTORE_LOGO = "https://www.gmodstore.com/favicon.ico"
