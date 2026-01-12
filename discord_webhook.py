"""
Discord Webhook Module
Sends job listings to Discord as embeds
"""

import requests
import time
from typing import Dict, List
import config


class DiscordWebhook:
    def __init__(self, webhook_url: str):
        """
        Initializes Discord webhook client
        
        Args:
            webhook_url: Discord webhook URL
        """
        self.webhook_url = webhook_url
        self.rate_limit_delay = 1  # Minimum wait time between messages (seconds)
    
    def send_job(self, job: Dict) -> bool:
        """
        Sends a single job listing to Discord
        
        Args:
            job: Job listing data
            
        Returns:
            bool: Success?
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
                print(f"[SUCCESS] Listing sent: {job['title']}")
                return True
            elif response.status_code == 429:
                # Rate limit
                retry_after = response.json().get('retry_after', 5)
                print(f"[WARNING] Rate limit! Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return self.send_job(job)  # Retry
            else:
                print(f"[ERROR] Discord webhook error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error sending listing: {e}")
            return False
    
    def send_jobs(self, jobs: List[Dict]) -> int:
        """
        Sends multiple job listings to Discord
        
        Args:
            jobs: List of job listings
            
        Returns:
            int: Number of successfully sent listings
        """
        sent_count = 0
        
        for job in jobs:
            if self.send_job(job):
                sent_count += 1
            
            # Rate limit protection
            time.sleep(self.rate_limit_delay)
        
        return sent_count
    
    def _create_embed(self, job: Dict) -> Dict:
        """
        Creates Discord embed for job listing
        
        Args:
            job: Job listing data
            
        Returns:
            Dict: Discord embed payload
        """
        # Status-based color
        color = config.STATUS_COLORS.get(job['status'], 0x3498DB)
        
        # Embed title and description
        title = job.get('title', 'New Job Listing')
        url = job.get('url', '')
        
        # Main description
        description = job.get('description', 'Description not available')
        
        # Embed object
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
        Returns appropriate emoji for status
        
        Args:
            status: Job status
            
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
        Tests if webhook is working
        
        Returns:
            bool: Is working?
        """
        try:
            test_embed = {
                "title": "🚀 GModStore Job Scraper Started",
                "description": "Scraper is running successfully and monitoring new job listings!",
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
                print("[SUCCESS] Webhook test successful!")
                return True
            else:
                print(f"[ERROR] Webhook test failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[ERROR] Webhook test error: {e}")
            return False


if __name__ == "__main__":
    # For testing
    if config.DISCORD_WEBHOOK_URL == "BURAYA_WEBHOOK_URL_GIRILECEK":
        print("ERROR: Set DISCORD_WEBHOOK_URL in config.py!")
    else:
        webhook = DiscordWebhook(config.DISCORD_WEBHOOK_URL)
        webhook.test_webhook()
        
        # Example listing send
        test_job = {
            "title": "Test Job Listing",
            "url": "https://www.gmodstore.com/jobmarket/jobs/test123",
            "description": "This is a test listing.",
            "budget": "$100.00",
            "category": "Gamemode",
            "status": "Apply",
            "applications": 5,
            "views": 50,
            "due_date": "2026-02-01"
        }
        webhook.send_job(test_job)
