from django.core.mail import send_mail
from celery import shared_task
from decouple import config
import logging
from kavenegar import (
    KavenegarAPI,
    APIException,
    HTTPException,
)

logger = logging.getLogger(__name__)


@shared_task
def send_html_email_task(subject: str ,html_email:str, recipient:str) -> None:
    send_mail(
        subject=subject,
        message='',
        html_message=html_email,
        from_email='your_email@gmail.com',
        recipient_list=[recipient],
    )


@shared_task
def send_sms_validation_code_task(receptor: str, token:str) -> None:
    try:
        api = KavenegarAPI(config('KAVENEGAR_API_KEY'))
        params = {
            'receptor': receptor,
            'template': config('KAVENEGAR_VALIDATION_TEMPLATE'),
            'token': token,
            'type': 'sms',
        }
        api.verify_lookup(params)

    except APIException as e:
        logger.error(f'SMS Service APIError: {str(e)}')
        logger.info(f'confirm code: {token}')

    except HTTPException as e:
        logger.error(f'SMS Service HTTPError: {str(e)}')
        logger.info(f'confirm code: {token}')
