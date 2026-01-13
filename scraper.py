"""
GModStore Job Market Scraper
Web scraping module - Fetches and parses job listings
"""

import os
import certifi
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime, timezone
import re
import time
import config


class JobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.USER_AGENT
        })
        self.request_delay = getattr(config, 'DETAIL_REQUEST_DELAY', 1.5)  # Delay between detail page requests
        
        # Configure SSL
        self.ca_bundle_path = self._configure_ssl()
        if self.ca_bundle_path:
            self.session.verify = self.ca_bundle_path

    def _configure_ssl(self) -> Optional[str]:
        """
        Configures SSL certificate bundle path.
        Checks if certifi's default path exists, if not, tries common system paths.
        """
        # 1. Check certifi default path
        certifi_path = certifi.where()
        if os.path.exists(certifi_path):
            return certifi_path
            
        print(f"[WARNING] Certifi path not found: {certifi_path}")
        
        # 2. Check common system CA bundle paths
        common_paths = [
            "/etc/ssl/certs/ca-certificates.crt", # Debian/Ubuntu/Gentoo etc.
            "/etc/pki/tls/certs/ca-bundle.crt",   # Fedora/RHEL 6
            "/etc/ssl/ca-bundle.pem",             # OpenSUSE
            "/etc/pki/tls/cacert.pem",            # OpenELEC
            "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem", # CentOS/RHEL 7
            "/usr/local/etc/ssl/cert.pem",        # FreeBSD
            "/etc/ssl/cert.pem",                  # macOS
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                print(f"[INFO] Using system CA bundle: {path}")
                return path
                
        print("[ERROR] Could not find a suitable TLS CA certificate bundle!")
        return None
    
    def fetch_jobs(self) -> List[Dict]:
        """
        Fetches job listings from GModStore job market page
        Also fetches detailed information for each job
        
        Returns:
            List[Dict]: List of job listings with full details
        """
        try:
            response = self.session.get(config.GMODSTORE_JOBS_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            jobs = self._parse_jobs(soup)
            
            # Fetch details for each job
            print(f"[INFO] Fetching details for {len(jobs)} jobs...")
            detailed_jobs = []
            
            for i, job in enumerate(jobs, 1):
                try:
                    print(f"[INFO] Fetching details ({i}/{len(jobs)}): {job['title'][:50]}...")
                    details = self.fetch_job_details(job['url'])
                    
                    if details:
                        # Merge basic info with detailed info
                        job.update(details)
                        
                        # Validate job (check due date, etc.)
                        if self._is_valid_job(job):
                            detailed_jobs.append(job)
                        else:
                            print(f"[INFO] Filtered out: {job['title'][:50]} (invalid or expired)")
                    else:
                        # If details fetch fails, still add basic info
                        if self._is_valid_job(job):
                            detailed_jobs.append(job)
                    
                    # Rate limiting
                    if i < len(jobs):
                        time.sleep(self.request_delay)
                        
                except Exception as e:
                    print(f"[WARNING] Error fetching details for job: {e}")
                    # Add job with basic info if detail fetch fails
                    if self._is_valid_job(job):
                        detailed_jobs.append(job)
                    continue
            
            return detailed_jobs
        
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
        Checks if a job listing is valid and not expired
        
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
        
        # Check if due date has passed
        if not self._is_due_date_valid(job.get('due_date')):
            return False
        
        return True
    
    def _is_due_date_valid(self, due_date_str: str) -> bool:
        """
        Checks if due date is valid (not passed)
        
        Args:
            due_date_str: Due date string from job listing
            
        Returns:
            bool: True if valid (not passed) or no due date, False if passed
        """
        if not due_date_str or due_date_str == "N/A" or due_date_str.lower() == "none":
            # No due date means it's still valid
            return True
        
        try:
            # Try to parse various date formats
            # GModStore typically uses format like "Jan 15, 2026" or "2026-01-15"
            date_formats = [
                "%Y-%m-%d %H:%M:%S",  # 2026-01-31 00:00:00
                "%Y-%m-%d",       # 2026-01-15
                "%b %d, %Y",      # Jan 15, 2026
                "%B %d, %Y",      # January 15, 2026
                "%d %b %Y",       # 15 Jan 2026
                "%d %B %Y",       # 15 January 2026
                "%m/%d/%Y",       # 01/15/2026
                "%d/%m/%Y",       # 15/01/2026
            ]
            
            due_date = None
            for fmt in date_formats:
                try:
                    due_date = datetime.strptime(due_date_str.strip(), fmt)
                    break
                except ValueError:
                    continue
            
            if not due_date:
                print(f"[WARNING] Could not parse due date: {due_date_str}")
                return True  # If we can't parse, don't filter it out
            
            # Compare with current date (use UTC to be safe)
            now = datetime.now()
            
            # Job is valid if due date is in the future or today
            is_valid = due_date.date() >= now.date()
            
            if not is_valid:
                print(f"[INFO] Job expired: due date was {due_date_str}")
            
            return is_valid
            
        except Exception as e:
            print(f"[WARNING] Error checking due date '{due_date_str}': {e}")
            return True  # If there's an error, don't filter it out
    
    def fetch_job_details(self, job_url: str) -> Dict:
        """
        Fetches detailed information of a single job listing
        
        Args:
            job_url: Job listing URL
            
        Returns:
            Dict: Detailed job listing data
        """
        details = {}
        
        try:
            response = self.session.get(job_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Description - Note: GModStore uses dynamic Vue.js rendering (v-quill-render)
            # The description content is loaded via JavaScript and not available in static HTML
            # For now, we'll create a descriptive summary from available data
            
            # Try to find any static text content that might be useful
            description_parts = []
            
            # Add budget if available
            if details.get('budget'):
                description_parts.append(f"Budget: {details['budget']}")
            
            # Add category if available
            if details.get('category'):
                description_parts.append(f"Category: {details['category']}")
            
            # Add application count
            if details.get('applications') is not None:
                app_count = details['applications']
                description_parts.append(f"{app_count} application{'s' if app_count != 1 else ''}")
            
            # Create basic description
            if description_parts:
                details['description'] = " | ".join(description_parts)
            
            # Note: To get full description, you would need to:
            # 1. Use Selenium/Playwright for JavaScript rendering
            # 2. Access GModStore API if available
            # 3. Parse from a different source
            # For this use case, the summary is sufficient for Discord notifications
            
            # Status - Look for job status badge/label
            status_elem = soup.find(['span', 'div'], class_=re.compile(r'job.*status|status.*badge', re.I))
            if status_elem:
                status_text = status_elem.get_text(strip=True)
                if status_text in config.ACTIVE_JOB_STATUSES + ["Finished"]:
                    details['status'] = status_text
            
            # Budget - Look for price/budget information
            budget_label = soup.find(string=re.compile(r'^Budget$', re.I))
            if budget_label:
                parent = budget_label.find_parent()
                if parent:
                    card = parent.find_parent('div', class_='card')
                    if card:
                        card_body = card.find('div', class_='card-body')
                        if card_body:
                            card_text = card_body.find('div', class_='card-text')
                            if card_text:
                                details['budget'] = card_text.get_text(strip=True)
            
            # Due Date - Multiple approaches
            due_date = None
            
            # Try 1: Look for "DUE DATE" text
            due_elem = soup.find(string=re.compile(r'DUE\s*DATE', re.I))
            if due_elem:
                # Find the next element with date info
                parent = due_elem.find_parent()
                if parent:
                    next_elem = parent.find_next(['span', 'div', 'time', 'dd'])
                    if next_elem:
                        due_date = next_elem.get_text(strip=True)
            
            # Try 2: Look for v-date-time with time attribute
            if not due_date:
                date_elem = soup.find('v-date-time', {'time': True})
                if date_elem:
                    due_date = date_elem.get('time')
            
            # Try 3: Look for time element
            if not due_date:
                time_elem = soup.find('time', {'datetime': True})
                if time_elem:
                    due_date = time_elem.get('datetime') or time_elem.get_text(strip=True)
            
            if due_date:
                details['due_date'] = due_date
            
            # Applications - Look for applicant count
            # First try to find "Applications" label and its value
            app_label = soup.find(string=re.compile(r'^Applications$', re.I))
            if app_label:
                parent = app_label.find_parent()
                if parent:
                    next_elem = parent.find_next(['dd', 'span', 'div'])
                    if next_elem:
                        app_text = next_elem.get_text(strip=True)
                        num_match = re.search(r'(\d+)', app_text)
                        if num_match:
                            details['applications'] = int(num_match.group(1))
            
            # Fallback: search in text
            if 'applications' not in details:
                app_patterns = [
                    (r'(\d+)\s*applicant', re.I),
                    (r'Applications[:\s]+(\d+)', re.I),
                ]
                
                for pattern, flags in app_patterns:
                    app_match = soup.find(string=re.compile(pattern, flags))
                    if app_match:
                        num_match = re.search(pattern, app_match, flags)
                        if num_match:
                            details['applications'] = int(num_match.group(1))
                            break
            
            # Views - Look for view count
            # First try to find "Views" label and its value
            views_label = soup.find(string=re.compile(r'^Views$', re.I))
            if views_label:
                parent = views_label.find_parent()
                if parent:
                    next_elem = parent.find_next(['dd', 'span', 'div'])
                    if next_elem:
                        views_text = next_elem.get_text(strip=True)
                        num_match = re.search(r'([\d,]+)', views_text)
                        if num_match:
                            view_str = num_match.group(1).replace(',', '')
                            details['views'] = int(view_str)
            
            # Fallback: search in text
            if 'views' not in details:
                view_patterns = [
                    (r'([\d,]+)\s*views?', re.I),
                    (r'Views[:\s]+([\d,]+)', re.I),
                ]
                
                for pattern, flags in view_patterns:
                    view_match = soup.find(string=re.compile(pattern, flags))
                    if view_match:
                        num_match = re.search(pattern, view_match, flags)
                        if num_match:
                            # Parse number with commas (e.g., "1,234")
                            view_str = num_match.group(1).replace(',', '')
                            details['views'] = int(view_str)
                            break
            
            # Category - Look for category information
            cat_elem = soup.find(string=re.compile(r'^Category$', re.I))
            if cat_elem:
                parent = cat_elem.find_parent()
                if parent:
                    # Try to find the next dd element (definition description) or a link
                    next_elem = parent.find_next(['dd', 'a'])
                    if next_elem:
                        cat_text = next_elem.get_text(strip=True)
                        # Clean up category - should be short like "Gamemode", "Modelling", etc.
                        if cat_text and len(cat_text) < 50 and not cat_text.startswith('Job:'):
                            details['category'] = cat_text
            
            return details
            
        except requests.Timeout:
            print(f"[WARNING] Timeout fetching job details: {job_url}")
            return {}
        except requests.RequestException as e:
            print(f"[WARNING] Request error fetching job details: {e}")
            return {}
        except Exception as e:
            print(f"[WARNING] Error parsing job details: {e}")
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
