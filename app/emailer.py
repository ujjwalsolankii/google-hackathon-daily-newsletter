import os
from google.cloud import firestore
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from news import fetch_top_items
from ai_client import generate_newsletter_text

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "example@gmail.com")

db = firestore.Client()
COLLECTION = "subscribers"

def send_email(to, html):
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to,
        subject="Daily Tech Newsletter",
        html_content=html
    )
    sg.send(message)

def send_newsletter_to_all():
    subscribers = [doc.to_dict()["email"] for doc in db.collection(COLLECTION).stream()]

    news_items = fetch_top_items()
    newsletter_html = generate_newsletter_text(news_items)

    for email in subscribers:
        send_email(email, newsletter_html)
