from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_html_email_task(subject: str ,html_email:str, recipient:str) -> None:
    send_mail(
        subject=subject,
        message='',
        html_message=html_email,
        from_email='your_email@gmail.com',
        recipient_list=[recipient],
    )
