"""
GModStore Job Market Scraper
Web scraping modülü - İş ilanlarını çeker ve parse eder
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import config


class JobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT
        })
    
    def fetch_jobs(self) -> List[Dict]:
        """
        GModStore job market sayfasından iş ilanlarını çeker
        
        Returns:
            List[Dict]: İş ilanları listesi
        """
        try:
            response = self.session.get(config.GMODSTORE_JOBS_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            jobs = self._parse_jobs(soup)
            
            return jobs
        
        except requests.RequestException as e:
            print(f"[ERROR] GModStore'a bağlanırken hata: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] İlanları parse ederken hata: {e}")
            return []
    
    def _parse_jobs(self, soup: BeautifulSoup) -> List[Dict]:
        """
        HTML'den iş ilanlarını parse eder
        
        Args:
            soup: BeautifulSoup nesnesi
            
        Returns:
            List[Dict]: Parse edilmiş iş ilanları
        """
        jobs = []
        
        # İş ilanı kartlarını bul - GModStore'un gerçek yapısına göre
        job_cards = soup.find_all('div', class_='item-listing item-listing--job')
        
        if not job_cards:
            print("[WARNING] 'item-listing--job' class'ı bulunamadı, alternatif deneniyor...")
            # Alternatif selector
            job_cards = soup.select('div.item-listing')
        
        print(f"[DEBUG] {len(job_cards)} iş kartı bulundu")
        
        for card in job_cards:
            try:
                job_data = self._extract_job_data(card)
                if job_data and self._is_valid_job(job_data):
                    jobs.append(job_data)
            except Exception as e:
                print(f"[WARNING] İlan parse edilirken hata: {e}")
                continue
        
        return jobs
    
    def _extract_job_data(self, card) -> Optional[Dict]:
        """
        Tek bir iş ilanı kartından veri çıkarır
        
        Args:
            card: BeautifulSoup element
            
        Returns:
            Dict: İlan verisi veya None
        """
        job = {}
        
        # URL çıkar (en önemli - unique identifier)
        link = card.find('a', class_='item-listing__link')
        if not link or not link.get('href'):
            return None
        
        href = link['href']
        if not href.startswith('http'):
            href = f"https://www.gmodstore.com{href}"
        
        # Job URL doğrulama - /jobmarket/jobs/ içermeli
        if '/jobmarket/jobs/' not in href:
            return None
            
        job['url'] = href
        job['job_id'] = href.split('/')[-1]
        
        # Başlık - item-listing__name div'inden al
        title_elem = card.find('div', class_='item-listing__name')
        if title_elem:
            # Önce title attribute'unu dene (tam başlık burada)
            job['title'] = title_elem.get('title', '').strip() or title_elem.get_text(strip=True)
        else:
            job['title'] = "Başlık bulunamadı"
        
        # "Post a job" gibi navigasyon elementlerini filtrele
        if job['title'].lower() in ['post a job', 'browse jobs', 'create job', '']:
            return None
        
        # Budget - item-listing__bottom__right__price div'inden al
        price_elem = card.find('div', class_='item-listing__bottom__right__price')
        if price_elem:
            job['budget'] = price_elem.get_text(strip=True)
        else:
            job['budget'] = "N/A"
        
        # Category ve Applications - card-body p elementinden parse et
        # Format: "Gamemode - 2 applicants"
        card_body = card.find('div', class_='card-body')
        if card_body:
            p_elem = card_body.find('p')
            if p_elem:
                body_text = p_elem.get_text(strip=True)
                # Category ve applicant sayısını ayır
                if ' - ' in body_text:
                    parts = body_text.rsplit(' - ', 1)
                    job['category'] = parts[0].strip()
                    # Applicant sayısını çıkar
                    app_match = re.search(r'(\d+)\s*applicant', parts[1], re.I)
                    job['applications'] = int(app_match.group(1)) if app_match else 0
                else:
                    job['category'] = body_text
                    job['applications'] = 0
            else:
                job['category'] = "N/A"
                job['applications'] = 0
        else:
            job['category'] = "N/A"
            job['applications'] = 0
        
        # Listeleme tarihi - v-date-time elementinden al
        date_elem = card.find('v-date-time')
        if date_elem and date_elem.get('time'):
            job['listed_date'] = date_elem['time']
        else:
            job['listed_date'] = "N/A"
        
        # Views (liste sayfasında mevcut değil, detay sayfasından alınabilir)
        job['views'] = 0
        
        # Description (liste sayfasında mevcut değil)
        job['description'] = f"Budget: {job['budget']} | Category: {job['category']} | Applications: {job['applications']}"
        
        # Due Date (liste sayfasında mevcut değil)
        job['due_date'] = "N/A"
        
        # Status - aktif ilanlar listede görünür, default "Apply"
        job['status'] = "Apply"
        
        return job
    
    def _is_valid_job(self, job: Dict) -> bool:
        """
        İş ilanının geçerli olup olmadığını kontrol eder
        
        Args:
            job: İş ilanı verisi
            
        Returns:
            bool: Geçerli mi?
        """
        # URL ve job_id olmalı
        if not job.get('url') or not job.get('job_id'):
            return False
        
        # Sadece aktif durumları kabul et
        if job.get('status') not in config.ACTIVE_JOB_STATUSES:
            return False
        
        # Başlık anlamlı olmalı
        title = job.get('title', '').lower()
        invalid_titles = ['post a job', 'browse jobs', 'create job', 'başlık bulunamadı', '']
        if title in invalid_titles:
            return False
        
        return True
    
    def fetch_job_details(self, job_url: str) -> Dict:
        """
        Tek bir iş ilanının detaylarını çeker
        Bu fonksiyon ihtiyaç halinde kullanılabilir
        
        Args:
            job_url: İlan URL'si
            
        Returns:
            Dict: Detaylı ilan verisi
        """
        try:
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Detaylı parsing yapılabilir
            details = {}
            
            # Budget
            budget_elem = soup.find(text=re.compile(r'Budget'))
            if budget_elem:
                details['budget'] = budget_elem.find_next().get_text(strip=True)
            
            # Category
            category_elem = soup.find(text=re.compile(r'Category'))
            if category_elem:
                details['category'] = category_elem.find_next().get_text(strip=True)
            
            # Applications
            app_elem = soup.find(text=re.compile(r'Applications'))
            if app_elem:
                app_text = app_elem.find_next().get_text(strip=True)
                app_num = re.search(r'(\d+)', app_text)
                details['applications'] = int(app_num.group(1)) if app_num else 0
            
            # Views
            views_elem = soup.find(text=re.compile(r'Views'))
            if views_elem:
                views_text = views_elem.find_next().get_text(strip=True)
                views_num = re.search(r'(\d+)', views_text)
                details['views'] = int(views_num.group(1)) if views_num else 0
            
            # Description
            desc_elem = soup.find(['div', 'section'], class_=re.compile(r'description|content', re.I))
            if desc_elem:
                details['description'] = desc_elem.get_text(strip=True)
            
            # Due Date
            due_elem = soup.find(text=re.compile(r'DUE DATE'))
            if due_elem:
                details['due_date'] = due_elem.find_next().get_text(strip=True)
            
            return details
            
        except Exception as e:
            print(f"[ERROR] İlan detayları çekilirken hata: {e}")
            return {}


if __name__ == "__main__":
    # Test için
    scraper = JobScraper()
    print("GModStore iş ilanları çekiliyor...")
    jobs = scraper.fetch_jobs()
    print(f"Toplam {len(jobs)} aktif ilan bulundu:")
    for job in jobs[:5]:  # İlk 5 tanesini göster
        print(f"  - {job['title']}")
        print(f"    Budget: {job['budget']}")
        print(f"    Category: {job['category']}")
        print(f"    Applications: {job['applications']}")
        print(f"    URL: {job['url']}")
        print()
