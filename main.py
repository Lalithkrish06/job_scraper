import sys
import time
from scraper.ai_job_scraper import AIJobScraper
from utils.csv_handler import CSVHandler
from utils.email_notifier import EmailNotifier

def main():
    print("="*60)
    print("🤖 AI JOB FINDER - TAMIL NADU 🤖")
    print("="*60)
    
    # Get user input
    job_title = input("\n💼 Enna job venum? (e.g., Data Analyst, Python Developer): ").strip()
    if not job_title:
        print("❌ Job title enter pannanum da!")
        return
    
    city = input("📍 Enna city? (e.g., Chennai, Madurai, Coimbatore): ").strip()
    if not city:
        print("❌ City enter pannanum da!")
        return
    
    # Tamil Nadu cities list for validation
    tn_cities = ["Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", 
                 "Tirunelveli", "Vellore", "Erode", "Tuticorin", "Nagercoil",
                 "Thanjavur", "Dindigul", "Karur", "Sivakasi", "Tiruppur"]
    
    # Warning if city not in TN (but still allow)
    city_found = any(c.lower() == city.lower() for c in tn_cities)
    if not city_found:
        print(f"⚠️ Warning: '{city}' Tamil Nadu list-la illa, but still try pannuren...")
    
    print(f"\n{'='*60}")
    print(f"🔍 Searching: '{job_title}' in '{city}'...")
    print(f"{'='*60}")
    
    scraper = AIJobScraper()
    
    try:
        jobs = scraper.scrape_all_sources(job_title, city)
        
        if not jobs:
            print(f"\n{'--'*20}")
            print(f"-- NO JOB FOUND! --")
            print(f"'{job_title}' ku '{city}' la job illa sir/madam !")
            print(f"{'--'*20}")
            print("\n💡 Try pannu ga sir/madam:")
            print(f"   1. Vera city try pannu (e.g., Chennai, Coimbatore)")
            print(f"   2. Vera job title try pannu (e.g., Data Scientist, Python Developer)")
            return
        
        # Remove duplicates
        unique_jobs = scraper.remove_duplicates(jobs)
        
        print(f"\n{'='*60}")
        print(f"🎉 KITTAACHI! {len(unique_jobs)} JOBS FOUND! 🎉")
        print(f"{'='*60}")
        
        # Display jobs
        print(f"\n📋 RESULTS FOR '{job_title.upper()}' IN {city.upper()}:\n")
        for i, job in enumerate(unique_jobs[:15], 1):
            salary = job.get('salary', 'Not disclosed')
            print(f"{i}. {job['title']}")
            print(f"   🏢 Company: {job['company']}")
            print(f"   💰 Salary: {salary}")
            print(f"   🔗 Source: {job['source']}")
            print(f"   🌐 Link: {job['link'][:70]}...")
            print("-" * 60)
        
        # Save to CSV
        csv_handler = CSVHandler(f"{job_title.replace(' ', '_')}_{city}_jobs.csv")
        csv_handler.save_jobs(unique_jobs)
        
        # Email option
        send_email = input("\n📧 Email-la pidaama? (yes/no): ").lower()
        if send_email in ['yes', 'y']:
            email = input("Enter email: ").strip()
            if email:
                notifier = EmailNotifier()
                notifier.send_job_alert(email, unique_jobs, f"{job_title} in {city}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Internet connection check pannu!")

if __name__ == "__main__":
    main()
