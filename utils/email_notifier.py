import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailNotifier:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = os.getenv("EMAIL_USERNAME", "your_email@gmail.com")
        self.password = os.getenv("EMAIL_PASSWORD", "your_app_password")
    
    def send_job_alert(self, to_email, jobs, category):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = f"🤖 {len(jobs)} AI Jobs Found in Tamil Nadu!"
            
            # Group by city
            city_groups = {}
            for job in jobs:
                city = job.get('location', 'Unknown').split(',')[0]
                if city not in city_groups:
                    city_groups[city] = []
                city_groups[city].append(job)
            
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
                    .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px; }}
                    .city-section {{ margin: 20px 0; }}
                    .city-title {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
                    .job-card {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 8px; background: #fafafa; }}
                    .job-title {{ color: #667eea; font-size: 18px; font-weight: bold; margin: 0; }}
                    .company {{ color: #555; font-weight: bold; }}
                    .salary {{ color: #28a745; font-weight: bold; }}
                    .btn {{ background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 10px; }}
                    .footer {{ text-align: center; color: #999; margin-top: 30px; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 AI Job Report</h1>
                        <p>{len(jobs)} Opportunities in Tamil Nadu</p>
                        <p>Generated on {jobs[0]['scraped_at'] if jobs else ''}</p>
                    </div>
            """
            
            for city, city_jobs in sorted(city_groups.items()):
                html += f'<div class="city-section"><h2 class="city-title">📍 {city} ({len(city_jobs)} jobs)</h2>'
                for job in city_jobs[:5]:  # Top 5 per city
                    salary_display = job.get('salary', 'Not disclosed')
                    if salary_display == "Not disclosed":
                        salary_display = "💰 Salary not disclosed"
                    
                    html += f"""
                    <div class="job-card">
                        <p class="job-title">{job['title']}</p>
                        <p class="company">🏢 {job['company']}</p>
                        <p>📍 {job['location']}</p>
                        <p class="salary">{salary_display}</p>
                        <p>Source: {job['source']}</p>
                        <a href="{job['link']}" class="btn">Apply Now</a>
                    </div>
                    """
                html += '</div>'
            
            html += """
                    <div class="footer">
                        <p>Good luck with your applications! 🚀</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email sent to {to_email}")
            
        except Exception as e:
            print(f"❌ Email error: {e}")
            print("💡 Check your email credentials in environment variables")
