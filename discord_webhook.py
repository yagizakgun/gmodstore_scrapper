"""
Discord Webhook Module
İş ilanlarını Discord'a embed olarak gönderir
"""

import requests
import time
from typing import Dict, List
import config


class DiscordWebhook:
    def __init__(self, webhook_url: str):
        """
        Discord webhook client'ı başlatır
        
        Args:
            webhook_url: Discord webhook URL'si
        """
        self.webhook_url = webhook_url
        self.rate_limit_delay = 1  # Mesajlar arası minimum bekleme süresi (saniye)
    
    def send_job(self, job: Dict) -> bool:
        """
        Tek bir iş ilanını Discord'a gönderir
        
        Args:
            job: İş ilanı verisi
            
        Returns:
            bool: Başarılı mı?
        """
        try:
            embed = self._create_embed(job)
            payload = {
                "embeds": [embed]
            }
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:
                print(f"[SUCCESS] İlan gönderildi: {job['title']}")
                return True
            elif response.status_code == 429:
                # Rate limit
                retry_after = response.json().get('retry_after', 5)
                print(f"[WARNING] Rate limit! {retry_after} saniye bekleniyor...")
                time.sleep(retry_after)
                return self.send_job(job)  # Tekrar dene
            else:
                print(f"[ERROR] Discord webhook hatası: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"[ERROR] İlan gönderilirken hata: {e}")
            return False
    
    def send_jobs(self, jobs: List[Dict]) -> int:
        """
        Birden fazla iş ilanını Discord'a gönderir
        
        Args:
            jobs: İş ilanları listesi
            
        Returns:
            int: Başarıyla gönderilen ilan sayısı
        """
        sent_count = 0
        
        for job in jobs:
            if self.send_job(job):
                sent_count += 1
            
            # Rate limit koruması
            time.sleep(self.rate_limit_delay)
        
        return sent_count
    
    def _create_embed(self, job: Dict) -> Dict:
        """
        İş ilanı için Discord embed oluşturur
        
        Args:
            job: İş ilanı verisi
            
        Returns:
            Dict: Discord embed payload
        """
        # Durum bazlı renk
        color = config.STATUS_COLORS.get(job['status'], 0x3498DB)
        
        # Embed başlığı ve açıklaması
        title = job.get('title', 'Yeni İş İlanı')
        url = job.get('url', '')
        
        # Ana açıklama
        description = job.get('description', 'Açıklama mevcut değil')
        
        # Embed nesnesi
        embed = {
            "title": title,
            "url": url,
            "description": description,
            "color": color,
            "thumbnail": {
                "url": config.GMODSTORE_LOGO
            },
            "fields": [],
            "footer": {
                "text": "GModStore Job Market"
            }
        }
        
        # Budget field
        if job.get('budget'):
            embed["fields"].append({
                "name": "💰 Budget",
                "value": job['budget'],
                "inline": True
            })
        
        # Category field
        if job.get('category'):
            embed["fields"].append({
                "name": "📁 Category",
                "value": job['category'],
                "inline": True
            })
        
        # Status field
        status_emoji = self._get_status_emoji(job['status'])
        embed["fields"].append({
            "name": "📊 Status",
            "value": f"{status_emoji} {job['status']}",
            "inline": True
        })
        
        # Applications field
        embed["fields"].append({
            "name": "📝 Applications",
            "value": str(job.get('applications', 0)),
            "inline": True
        })
        
        # Views field
        embed["fields"].append({
            "name": "👁️ Views",
            "value": str(job.get('views', 0)),
            "inline": True
        })
        
        # Due Date field
        if job.get('due_date') and job['due_date'] != "N/A":
            embed["fields"].append({
                "name": "⏰ Due Date",
                "value": job['due_date'],
                "inline": True
            })
        
        return embed
    
    def _get_status_emoji(self, status: str) -> str:
        """
        Durum için uygun emoji döndürür
        
        Args:
            status: İş durumu
            
        Returns:
            str: Emoji
        """
        emoji_map = {
            "Apply": "🟢",
            "In Progress": "🟡",
            "Negotiations": "🟠",
            "Finished": "⚫"
        }
        return emoji_map.get(status, "🔵")
    
    def test_webhook(self) -> bool:
        """
        Webhook'un çalışıp çalışmadığını test eder
        
        Returns:
            bool: Çalışıyor mu?
        """
        try:
            test_embed = {
                "title": "🚀 GModStore Job Scraper Başlatıldı",
                "description": "Scraper başarıyla çalışıyor ve yeni iş ilanlarını izliyor!",
                "color": 0x00FF00,
                "footer": {
                    "text": "GModStore Job Market Scraper"
                }
            }
            
            payload = {"embeds": [test_embed]}
            
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 204:
                print("[SUCCESS] Webhook test başarılı!")
                return True
            else:
                print(f"[ERROR] Webhook test başarısız: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Webhook test hatası: {e}")
            return False


if __name__ == "__main__":
    # Test için
    if config.DISCORD_WEBHOOK_URL == "BURAYA_WEBHOOK_URL_GIRILECEK":
        print("HATA: config.py dosyasında DISCORD_WEBHOOK_URL'yi ayarlayın!")
    else:
        webhook = DiscordWebhook(config.DISCORD_WEBHOOK_URL)
        webhook.test_webhook()
        
        # Örnek ilan gönderimi
        test_job = {
            "title": "Test İş İlanı",
            "url": "https://www.gmodstore.com/jobmarket/jobs/test123",
            "description": "Bu bir test ilanıdır.",
            "budget": "$100.00",
            "category": "Gamemode",
            "status": "Apply",
            "applications": 5,
            "views": 50,
            "due_date": "2026-02-01"
        }
        webhook.send_job(test_job)
