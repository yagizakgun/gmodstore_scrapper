"""
GModStore Job Market Discord Scraper
Main application - Checks job listings and sends them to Discord
"""

import json
import time
import signal
import sys
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, List

import config
from scraper import JobScraper
from discord_webhook import DiscordWebhook


class JobScraperBot:
    def __init__(self):
        """Initializes the scraper bot"""
        self.scraper = JobScraper()
        self.webhook = DiscordWebhook(config.DISCORD_WEBHOOK_URL)
        self.seen_jobs_file = Path("seen_jobs.json")
        self.seen_jobs: Set[str] = self._load_seen_jobs()
        self.running = True
        
        # Signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_seen_jobs(self) -> Set[str]:
        """
        Loads previously seen job listings
        
        Returns:
            Set[str]: Seen listing IDs
        """
        if self.seen_jobs_file.exists():
            try:
                with open(self.seen_jobs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"[INFO] Loaded {len(data)} seen listings")
                    return set(data)
            except Exception as e:
                print(f"[WARNING] Could not load seen listings: {e}")
                return set()
        else:
            print("[INFO] New seen_jobs.json file will be created")
            return set()
    
    def _save_seen_jobs(self):
        """Saves seen job listings"""
        try:
            with open(self.seen_jobs_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.seen_jobs), f, indent=2)
            print(f"[INFO] Saved {len(self.seen_jobs)} listings")
        except Exception as e:
            print(f"[ERROR] Could not save seen listings: {e}")
    
    def _signal_handler(self, signum, frame):
        """
        Graceful shutdown handler (Ctrl+C)
        
        Args:
            signum: Signal number
            frame: Frame object
        """
        print("\n[INFO] Shutdown signal received. Cleaning up...")
        self.running = False
        self._save_seen_jobs()
        print("[INFO] Scraper closed. Goodbye!")
        sys.exit(0)
    
    def check_and_send_new_jobs(self) -> int:
        """
        Checks for new job listings and sends them to Discord
        
        Returns:
            int: Number of new listings sent
        """
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking listings...")
        
        # Fetch listings
        jobs = self.scraper.fetch_jobs()
        
        if not jobs:
            print("[WARNING] No listings found or an error occurred")
            return 0
        
        print(f"[INFO] Found {len(jobs)} active listings")
        
        # Filter new listings
        new_jobs = []
        for job in jobs:
            job_id = job.get('job_id')
            if job_id and job_id not in self.seen_jobs:
                new_jobs.append(job)
                self.seen_jobs.add(job_id)
        
        if not new_jobs:
            print("[INFO] No new listings")
            return 0
        
        print(f"[INFO] Found {len(new_jobs)} new listings!")
        
        # Send new listings to Discord
        sent_count = self.webhook.send_jobs(new_jobs)
        
        # Save seen listings
        self._save_seen_jobs()
        
        print(f"[SUCCESS] {sent_count}/{len(new_jobs)} listings sent successfully")
        
        return sent_count
    
    def run(self):
        """
        Main loop - Checks listings at regular intervals
        """
        print("=" * 60)
        print("GModStore Job Market Discord Scraper")
        print("=" * 60)
        print(f"Check interval: {config.CHECK_INTERVAL} seconds ({config.CHECK_INTERVAL // 60} minutes)")
        print(f"Target URL: {config.GMODSTORE_JOBS_URL}")
        print("Starting...\n")
        
        # Webhook test
        if config.DISCORD_WEBHOOK_URL == "BURAYA_WEBHOOK_URL_GIRILECEK":
            print("[ERROR] Set DISCORD_WEBHOOK_URL in config.py!")
            print("Exiting...")
            sys.exit(1)
        
        print("[INFO] Testing Discord webhook...")
        if not self.webhook.test_webhook():
            print("[ERROR] Webhook test failed! Check the URL.")
            # In headless/service mode input() doesn't work, continue automatically
            if sys.stdin.isatty():
                print("Do you want to continue? (y/N): ", end='')
                response = input().strip().lower()
                if response != 'y':
                    sys.exit(1)
            else:
                print("[WARNING] Running in service mode, continuing...")
                time.sleep(5)
        
        print("\n[INFO] Bot started. Press Ctrl+C to stop.\n")
        
        # Perform first check immediately
        try:
            self.check_and_send_new_jobs()
        except Exception as e:
            print(f"[ERROR] Error during first check: {e}")
        
        # Main loop
        while self.running:
            try:
                # Wait until next check
                print(f"\n[INFO] Next check: in {config.CHECK_INTERVAL} seconds...")
                time.sleep(config.CHECK_INTERVAL)
                
                # Perform check
                self.check_and_send_new_jobs()
                
            except KeyboardInterrupt:
                # Ctrl+C - signal handler will catch
                break
            except Exception as e:
                print(f"[ERROR] Unexpected error: {e}")
                print("[INFO] Will retry in 60 seconds...")
                time.sleep(60)


def main():
    """Main function"""
    try:
        bot = JobScraperBot()
        bot.run()
    except Exception as e:
        print(f"[FATAL ERROR] Application could not be started: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
