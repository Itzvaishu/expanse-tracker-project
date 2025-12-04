from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME = "vaishuverma804@gmail.com",      
    MAIL_PASSWORD = "klex nknp bucr nxiz",         
    MAIL_FROM = "your-email@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_otp_email(email_to: str, otp: str):
    html = f"""
    <h3>Password Reset Request</h3>
    <p>Your OTP for password reset is:</p>
    <h2 style="color: blue;">{otp}</h2>
    <p>This OTP is valid for 10 minutes.</p>
    """

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email_to],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)