import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Environment variables load karein
# load_dotenv()  # Commented out since config.py already loads .env

def send_password_change_email(to_email: str, username: str):
    sender_email = os.getenv("GMAIL_EMAIL")
    sender_password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender_email or not sender_password:
        print("Error: Gmail credentials not found in .env file")
        return

    subject = "Security Alert: Password Changed"
    body = f"""
    <html>
    <body>
        <h2>Hello {username},</h2>
        <p>Your password for the <b>Expense Tracker App</b> was successfully changed just now.</p>
        <p>If this wasn't you, please contact the admin immediately.</p>
        <br>
        <p>Regards,<br>Tracker Team</p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        # Connect to Gmail SMTP Server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")