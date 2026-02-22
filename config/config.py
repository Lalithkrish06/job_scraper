import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use App Password for Gmail

# Scraping Configuration
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Filters
DEFAULT_LOCATION = "Chennai"
DEFAULT_SKILLS = ["Python", "Django", "Flask"]
