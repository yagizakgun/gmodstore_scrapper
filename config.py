# GModStore Job Scraper Configuration

# Discord Webhook URL - BURAYA WEBHOOK URL'NİZİ YAPIŞTIRIN
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1460186248068206664/RuCATGIxOpiV8EgNJ0mxkVorcTP9173rqq4ALwAYTtWx4KeQtP9L-lqkC9nKg4KMWEMa"

# Kontrol aralığı (saniye cinsinden)
CHECK_INTERVAL = 1800  # 30 dakika

# GModStore iş ilanları URL'si
GMODSTORE_JOBS_URL = "https://www.gmodstore.com/jobmarket/jobs/browse"

# User-Agent (bot algılamasını önlemek için)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Aktif iş durumları (sadece bunlar gönderilecek)
ACTIVE_JOB_STATUSES = ["Apply", "In Progress", "Negotiations"]

# Discord embed renkleri (durum bazında)
STATUS_COLORS = {
    "Apply": 0x00FF00,        # Yeşil
    "In Progress": 0xFFFF00,  # Sarı
    "Negotiations": 0xFFA500, # Turuncu
    "Finished": 0x808080      # Gri
}

# GModStore logo URL
GMODSTORE_LOGO = "https://www.gmodstore.com/favicon.ico"
