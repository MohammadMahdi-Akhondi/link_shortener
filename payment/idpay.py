import requests
import json


class APIException(Exception):
    pass


class HTTPException(Exception):
    pass


class IDPayAPI(object):
    def __init__(self, apikey, sandbox):
        self.version = 'v1.1/'
        self.domain = 'api.idpay.ir/'
        self.apikey = apikey
        self.sandbox = sandbox
        self.header = {
            'Content-Type': 'application/json',
            'X-API-KEY': apikey,
            'X-SANDBOX': '1' if sandbox else '0',
        }
    
    def __str__(self):
        return f'IDPay.APIKEY={self.apikey}'

    def _request(self, action='payment/', method='', data={}):
        url = 'https://' + self.domain + self.version + action + method
        try:
            response = requests.post(url=url, headers=self.header, data=json.dumps(data))
            error_status_codes = list(range(400, 406))
            if response.status_code in error_status_codes:
                raise APIException(f'status code: {response.status_code} detail:{response.json()}')

            return response.json()

        except requests.exceptions.RequestException as error:
            raise HTTPException(error)
    
    def create_transaction(self, data=None) -> dict:
        return self._request(action='payment', data=data)
    
    def confirm_transaction(self, data=None) -> dict:
        return self._request(method='verify', data=data)
