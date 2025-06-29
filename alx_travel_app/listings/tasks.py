from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

@shared_task
def send_payment_confirmation_email(email, reference):
    subject = "Booking Payment Confirmed"
    message = f"Your booking {reference} has been paid successfully."
    html_message = render_to_string("emails/payment_confirmation.html", {"reference": reference})

    send_mail(subject, message, 'noreply@example.com', [email], html_message=html_message)
