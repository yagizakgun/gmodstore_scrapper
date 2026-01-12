"""
GModStore Job Market Scraper
Web scraping module - Fetches and parses job listings
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
        Fetches job listings from GModStore job market page
        
        Returns:
            List[Dict]: List of job listings
        """
        try:
            response = self.session.get(config.GMODSTORE_JOBS_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            jobs = self._parse_jobs(soup)
            
            return jobs
        
        except requests.RequestException as e:
            print(f"[ERROR] Error connecting to GModStore: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] Error parsing listings: {e}")
            return []
    
    def _parse_jobs(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parses job listings from HTML
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List[Dict]: Parsed job listings
        """
        jobs = []
        
        # Find job listing cards - according to GModStore's actual structure
        job_cards = soup.find_all('div', class_='item-listing item-listing--job')
        
        if not job_cards:
            print("[WARNING] 'item-listing--job' class not found, trying alternative...")
            # Alternative selector
            job_cards = soup.select('div.item-listing')
        
        print(f"[DEBUG] Found {len(job_cards)} job cards")
        
        for card in job_cards:
            try:
                job_data = self._extract_job_data(card)
                if job_data and self._is_valid_job(job_data):
                    jobs.append(job_data)
            except Exception as e:
                print(f"[WARNING] Error parsing listing: {e}")
                continue
        
        return jobs
    
    def _extract_job_data(self, card) -> Optional[Dict]:
        """
        Extracts data from a single job listing card
        
        Args:
            card: BeautifulSoup element
            
        Returns:
            Dict: Job listing data or None
        """
        job = {}
        
        # Extract URL (most important - unique identifier)
        link = card.find('a', class_='item-listing__link')
        if not link or not link.get('href'):
            return None
        
        href = link['href']
        if not href.startswith('http'):
            href = f"https://www.gmodstore.com{href}"
        
        # Job URL validation - must contain /jobmarket/jobs/
        if '/jobmarket/jobs/' not in href:
            return None
            
        job['url'] = href
        job['job_id'] = href.split('/')[-1]
        
        # Title - get from item-listing__name div
        title_elem = card.find('div', class_='item-listing__name')
        if title_elem:
            # Try title attribute first (full title is here)
            job['title'] = title_elem.get('title', '').strip() or title_elem.get_text(strip=True)
        else:
            job['title'] = "Title not found"
        
        # Filter navigation elements like "Post a job"
        if job['title'].lower() in ['post a job', 'browse jobs', 'create job', '']:
            return None
        
        # Budget - get from item-listing__bottom__right__price div
        price_elem = card.find('div', class_='item-listing__bottom__right__price')
        if price_elem:
            job['budget'] = price_elem.get_text(strip=True)
        else:
            job['budget'] = "N/A"
        
        # Category and Applications - parse from card-body p element
        # Format: "Gamemode - 2 applicants"
        card_body = card.find('div', class_='card-body')
        if card_body:
            p_elem = card_body.find('p')
            if p_elem:
                body_text = p_elem.get_text(strip=True)
                # Separate category and applicant count
                if ' - ' in body_text:
                    parts = body_text.rsplit(' - ', 1)
                    job['category'] = parts[0].strip()
                    # Extract applicant count
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
        
        # Listing date - get from v-date-time element
        date_elem = card.find('v-date-time')
        if date_elem and date_elem.get('time'):
            job['listed_date'] = date_elem['time']
        else:
            job['listed_date'] = "N/A"
        
        # Views (not available on listing page, can be fetched from detail page)
        job['views'] = 0
        
        # Description (not available on listing page)
        job['description'] = f"Budget: {job['budget']} | Category: {job['category']} | Applications: {job['applications']}"
        
        # Due Date (not available on listing page)
        job['due_date'] = "N/A"
        
        # Status - active listings appear in list, default "Apply"
        job['status'] = "Apply"
        
        return job
    
    def _is_valid_job(self, job: Dict) -> bool:
        """
        Checks if a job listing is valid
        
        Args:
            job: Job listing data
            
        Returns:
            bool: Is valid?
        """
        # Must have URL and job_id
        if not job.get('url') or not job.get('job_id'):
            return False
        
        # Only accept active statuses
        if job.get('status') not in config.ACTIVE_JOB_STATUSES:
            return False
        
        # Title must be meaningful
        title = job.get('title', '').lower()
        invalid_titles = ['post a job', 'browse jobs', 'create job', 'title not found', '']
        if title in invalid_titles:
            return False
        
        return True
    
    def fetch_job_details(self, job_url: str) -> Dict:
        """
        Fetches details of a single job listing
        This function can be used when needed
        
        Args:
            job_url: Job listing URL
            
        Returns:
            Dict: Detailed job listing data
        """
        try:
            response = self.session.get(job_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Detailed parsing can be done
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
            print(f"[ERROR] Error fetching listing details: {e}")
            return {}


if __name__ == "__main__":
    # For testing
    scraper = JobScraper()
    print("Fetching GModStore job listings...")
    jobs = scraper.fetch_jobs()
    print(f"Found {len(jobs)} active listings:")
    for job in jobs[:5]:  # Show first 5
        print(f"  - {job['title']}")
        print(f"    Budget: {job['budget']}")
        print(f"    Category: {job['category']}")
        print(f"    Applications: {job['applications']}")
        print(f"    URL: {job['url']}")
        print()
