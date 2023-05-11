from rest_framework.exceptions import APIException
from . import messages


class UserNotCreated(APIException):
    status_code = 500
    default_detail = messages.USER_NOT_REGISTERED
    default_code = 'user_not_registered'


class TokenExpired(APIException):
    status_code = 400
    default_detail = messages.TOKEN_EXPIRED
    default_code = 'token_expired'


class SMS_NOT_SENT(APIException):
    status_code = 500
    default_detail = messages.SOMETHING_WENT_WRONG
    default_code = 'sms_not_sent'
