from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings

@shared_task
def send_email_task(subject, message, to_email):
    send_mail(
        subject=subject,
        message=message,
        from_email=['amineratit6@gmail.com'],
        recipient_list=[to_email],
        fail_silently=False,
    )

@shared_task
def broadcast_send_email_task(subject, message, to_email):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])

    