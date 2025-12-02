from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List

# --- APNA GMAIL CONFIG YAHAN DAALEIN --- (Same as in utils/email.py)
conf = ConnectionConfig(
    MAIL_USERNAME = "your-email@gmail.com",      
    MAIL_PASSWORD = "your-app-password",         
    MAIL_FROM = "your-email@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_password_change_email(email_to: str, username: str):
    html = f"""
    <h3>Password Changed Successfully</h3>
    <p>Dear {username},</p>
    <p>Your password has been changed successfully.</p>
    <p>If you did not make this change, please contact support immediately.</p>
    <p>Best regards,<br>Expense Tracker Team</p>
    """

    message = MessageSchema(
        subject="Password Changed Notification",
        recipients=[email_to],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
