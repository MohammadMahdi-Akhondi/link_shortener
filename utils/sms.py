from decouple import config
from kavenegar import (
    KavenegarAPI,
    APIException,
    HTTPException,
)


def send_validation_code(receptor: str, token:str):
    try:
        api = KavenegarAPI(config('KAVENEGAR_API_KEY'))
        params = {
            'receptor': receptor,
            'template': config('KAVENEGAR_VALIDATION_TEMPLATE'),
            'token': token,
            'type': 'sms',
        }
        api.verify_lookup(params)
        return True


    # TODO: Save log errors
    except APIException as e:
        print(e)

    except HTTPException as e:
        print(e)

    return False
