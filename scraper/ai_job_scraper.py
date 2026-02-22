import requests
from bs4 import BeautifulSoup
import time
import random
import re
from urllib.parse import quote

class AIJobScraper:
    def __init__(self):
        self.session = requests.Session()
        self.jobs = []
        
        # Rotate multiple user agents
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.536 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        ]
    
    def get_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
    
    def scrape_all_sources(self, keyword, location):
        """Try multiple sources"""
        jobs = []
        
        # Try LinkedIn (usually more open)
        try:
            linkedin_jobs = self.scrape_linkedin(keyword, location)
            jobs.extend(linkedin_jobs)
            print(f"   ✅ LinkedIn: {len(linkedin_jobs)} jobs")
        except Exception as e:
            print(f"   ⚠️ LinkedIn failed: {str(e)[:50]}")
        
        # Try Shine.com (good for India)
        try:
            shine_jobs = self.scrape_shine(keyword, location)
            jobs.extend(shine_jobs)
            print(f"   ✅ Shine: {len(shine_jobs)} jobs")
        except Exception as e:
            print(f"   ⚠️ Shine failed")
        
        # Try TimesJobs
        try:
            times_jobs = self.scrape_timesjobs(keyword, location)
            jobs.extend(times_jobs)
            print(f"   ✅ TimesJobs: {len(times_jobs)} jobs")
        except:
            pass
            
        return jobs
    
    def scrape_linkedin(self, keyword, location):
        """Scrape LinkedIn jobs"""
        jobs = []
        location_id = self._get_linkedin_location_id(location)
        
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={quote(keyword)}&location={quote(location)}&f_TPR=r86400&start=0"
        
        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='base-card')
            
            for card in job_cards[:10]:
                title_elem = card.find('h3', class_='base-search-card__title')
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                location_elem = card.find('span', class_='job-search-card__location')
                link_elem = card.find('a', class_='base-card__full-link')
                salary_elem = card.find('span', class_='job-search-card__salary-info')
                
                if title_elem and company_elem:
                    job = {
                        "title": title_elem.text.strip(),
                        "company": company_elem.text.strip(),
                        "location": location_elem.text.strip() if location_elem else location,
                        "salary": salary_elem.text.strip() if salary_elem else "Not disclosed",
                        "job_type": "Full Time",
                        "summary": f"AI/ML Role at {company_elem.text.strip()}",
                        "link": link_elem['href'] if link_elem else "https://linkedin.com/jobs",
                        "source": "LinkedIn",
                        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    jobs.append(job)
            
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            pass
        
        return jobs
    
    def scrape_shine(self, keyword, location):
        """Scrape Shine.com"""
        jobs = []
        url = f"https://www.shine.com/job-search/{keyword.replace(' ', '-')}-jobs-in-{location.lower()}"
        
        try:
            headers = self.get_headers()
            headers['Referer'] = 'https://www.shine.com/'
            
            response = self.session.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', class_='jobCard') or soup.find_all('div', class_='w-90')
            
            for card in job_cards[:8]:
                title = card.find('a', class_='job-title') or card.find('h2')
                company = card.find('span', class_='job-company') or card.find('div', class_='company-name')
                loc = card.find('span', class_='job-location') or card.find('div', class_='location')
                salary = card.find('span', class_='salary') or card.find('div', class_='package')
                
                if title:
                    jobs.append({
                        "title": title.text.strip(),
                        "company": company.text.strip() if company else "Unknown",
                        "location": loc.text.strip() if loc else location,
                        "salary": salary.text.strip() if salary else "Not disclosed",
                        "job_type": "Full Time",
                        "summary": "Click link for details",
                        "link": "https://www.shine.com" + title.get('href', '') if title.get('href') else url,
                        "source": "Shine",
                        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            time.sleep(random.uniform(2, 3))
        except:
            pass
        
        return jobs
    
    def scrape_timesjobs(self, keyword, location):
        """Scrape TimesJobs"""
        jobs = []
        url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords={quote(keyword)}&cboWorkExp1=-1&txtLocation={quote(location)}"
        
        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_list = soup.find_all('li', class_='clearfix joblistli')
            
            for job in job_list[:8]:
                title = job.find('h2')
                company = job.find('span', class_='company-name')
                loc = job.find('span', title=True)
                salary = job.find('span', class_='salary')
                
                if title:
                    link = title.find('a')['href'] if title.find('a') else url
                    jobs.append({
                        "title": title.text.strip(),
                        "company": company.text.strip() if company else "Unknown",
                        "location": loc['title'] if loc and loc.has_attr('title') else location,
                        "salary": salary.text.strip() if salary else "Not disclosed",
                        "job_type": "Full Time",
                        "summary": "TimesJobs listing",
                        "link": link,
                        "source": "TimesJobs",
                        "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            time.sleep(random.uniform(2, 3))
        except:
            pass
        
        return jobs
    
    def _get_linkedin_location_id(self, location):
        # Simplified mapping for major TN cities
        mapping = {
            "chennai": "106888327", "coimbatore": "105556700", 
            "madurai": "105901437", "trichy": "107000000"
        }
        return mapping.get(location.lower(), "")
    
    def remove_duplicates(self, jobs):
        """Remove duplicate jobs by title+company"""
        seen = set()
        unique = []
        for job in jobs:
            key = f"{job['title']}-{job['company']}"
            if key not in seen:
                seen.add(key)
                unique.append(job)
        return unique
