from rest_framework.exceptions import APIException
from . import messages


class UserNotCreated(APIException):
    status_code = 500
    default_detail = messages.USER_NOT_REGISTERED
    default_code = 'user_not_registered'
