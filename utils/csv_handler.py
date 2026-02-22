import pandas as pd
import os
from datetime import datetime

class CSVHandler:
    def __init__(self, filename="ai_jobs_tamilnadu.csv"):
        self.filename = filename
    
    def save_jobs(self, jobs):
        if not jobs:
            return
        
        # Clean salary data
        for job in jobs:
            if 'salary' not in job:
                job['salary'] = "Not disclosed"
        
        df = pd.DataFrame(jobs)
        
        # Reorder columns
        columns = ['title', 'company', 'location', 'salary', 'job_type', 'source', 'link', 'summary', 'scraped_at']
        df = df[[col for col in columns if col in df.columns]]
        
        if os.path.exists(self.filename):
            existing = pd.read_csv(self.filename)
            combined = pd.concat([existing, df]).drop_duplicates(subset=['title', 'company'])
            combined.to_csv(self.filename, index=False)
        else:
            df.to_csv(self.filename, index=False)
        
        print(f"\n💾 Saved to {self.filename} ({len(jobs)} jobs)")
