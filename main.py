"""
GModStore Job Market Discord Scraper
Ana uygulama - İş ilanlarını kontrol eder ve Discord'a gönderir
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
        """Scraper bot'u başlatır"""
        self.scraper = JobScraper()
        self.webhook = DiscordWebhook(config.DISCORD_WEBHOOK_URL)
        self.seen_jobs_file = Path("seen_jobs.json")
        self.seen_jobs: Set[str] = self._load_seen_jobs()
        self.running = True
        
        # Graceful shutdown için signal handler
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_seen_jobs(self) -> Set[str]:
        """
        Daha önce görülen iş ilanlarını yükler
        
        Returns:
            Set[str]: Görülen ilan ID'leri
        """
        if self.seen_jobs_file.exists():
            try:
                with open(self.seen_jobs_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"[INFO] {len(data)} görülmüş ilan yüklendi")
                    return set(data)
            except Exception as e:
                print(f"[WARNING] Görülen ilanlar yüklenemedi: {e}")
                return set()
        else:
            print("[INFO] Yeni seen_jobs.json dosyası oluşturulacak")
            return set()
    
    def _save_seen_jobs(self):
        """Görülen iş ilanlarını kaydeder"""
        try:
            with open(self.seen_jobs_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.seen_jobs), f, indent=2)
            print(f"[INFO] {len(self.seen_jobs)} ilan kaydedildi")
        except Exception as e:
            print(f"[ERROR] Görülen ilanlar kaydedilemedi: {e}")
    
    def _signal_handler(self, signum, frame):
        """
        Graceful shutdown handler (Ctrl+C)
        
        Args:
            signum: Signal numarası
            frame: Frame nesnesi
        """
        print("\n[INFO] Kapatma sinyali alındı. Temizlik yapılıyor...")
        self.running = False
        self._save_seen_jobs()
        print("[INFO] Scraper kapatıldı. Güle güle!")
        sys.exit(0)
    
    def check_and_send_new_jobs(self) -> int:
        """
        Yeni iş ilanlarını kontrol eder ve Discord'a gönderir
        
        Returns:
            int: Gönderilen yeni ilan sayısı
        """
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] İlanlar kontrol ediliyor...")
        
        # İlanları çek
        jobs = self.scraper.fetch_jobs()
        
        if not jobs:
            print("[WARNING] Hiç ilan bulunamadı veya bir hata oluştu")
            return 0
        
        print(f"[INFO] {len(jobs)} aktif ilan bulundu")
        
        # Yeni ilanları filtrele
        new_jobs = []
        for job in jobs:
            job_id = job.get('job_id')
            if job_id and job_id not in self.seen_jobs:
                new_jobs.append(job)
                self.seen_jobs.add(job_id)
        
        if not new_jobs:
            print("[INFO] Yeni ilan yok")
            return 0
        
        print(f"[INFO] {len(new_jobs)} yeni ilan bulundu!")
        
        # Yeni ilanları Discord'a gönder
        sent_count = self.webhook.send_jobs(new_jobs)
        
        # Görülen ilanları kaydet
        self._save_seen_jobs()
        
        print(f"[SUCCESS] {sent_count}/{len(new_jobs)} ilan başarıyla gönderildi")
        
        return sent_count
    
    def run(self):
        """
        Ana döngü - Belirli aralıklarla ilanları kontrol eder
        """
        print("=" * 60)
        print("GModStore Job Market Discord Scraper")
        print("=" * 60)
        print(f"Kontrol aralığı: {config.CHECK_INTERVAL} saniye ({config.CHECK_INTERVAL // 60} dakika)")
        print(f"Hedef URL: {config.GMODSTORE_JOBS_URL}")
        print("Başlatılıyor...\n")
        
        # Webhook testi
        if config.DISCORD_WEBHOOK_URL == "BURAYA_WEBHOOK_URL_GIRILECEK":
            print("[ERROR] config.py dosyasında DISCORD_WEBHOOK_URL'yi ayarlayın!")
            print("Çıkış yapılıyor...")
            sys.exit(1)
        
        print("[INFO] Discord webhook test ediliyor...")
        if not self.webhook.test_webhook():
            print("[ERROR] Webhook testi başarısız! URL'yi kontrol edin.")
            # Headless/service modunda input() çalışmaz, otomatik devam et
            if sys.stdin.isatty():
                print("Devam etmek istiyor musunuz? (y/N): ", end='')
                response = input().strip().lower()
                if response != 'y':
                    sys.exit(1)
            else:
                print("[WARNING] Service modunda çalışıyor, devam ediliyor...")
                time.sleep(5)
        
        print("\n[INFO] Bot başlatıldı. Ctrl+C ile durdurun.\n")
        
        # İlk kontrol hemen yapılsın
        try:
            self.check_and_send_new_jobs()
        except Exception as e:
            print(f"[ERROR] İlk kontrol sırasında hata: {e}")
        
        # Ana döngü
        while self.running:
            try:
                # Sonraki kontrole kadar bekle
                print(f"\n[INFO] Sonraki kontrol: {config.CHECK_INTERVAL} saniye sonra...")
                time.sleep(config.CHECK_INTERVAL)
                
                # Kontrol yap
                self.check_and_send_new_jobs()
                
            except KeyboardInterrupt:
                # Ctrl+C - signal handler yakalayacak
                break
            except Exception as e:
                print(f"[ERROR] Beklenmeyen hata: {e}")
                print("[INFO] 60 saniye sonra tekrar denenecek...")
                time.sleep(60)


def main():
    """Ana fonksiyon"""
    try:
        bot = JobScraperBot()
        bot.run()
    except Exception as e:
        print(f"[FATAL ERROR] Uygulama başlatılamadı: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
