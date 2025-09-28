from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging

logger = logging.getLogger("tasks")
email_logger = logging.getLogger("emails")

def send_email_to_admin(subject, message, from_email, name):
    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=["info@ctblackpros.co.za"]
        )
        if not email.send():
            return f"Email not sent from {from_email}"
        else:
            return "Email sent"
    except Exception as ex:
        email_logger.error(ex)
