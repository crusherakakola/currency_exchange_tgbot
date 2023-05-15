import requests
import json
from security import api


class APIException(Exception):
    pass


class Request:
    def __init__(self, base, quote, amount):
        self._base = base
        self._quote = quote
        self._amount = amount

    def get_price(self):
        url = f"https://api.apilayer.com/currency_data/convert?to={self._quote}&from={self._base}&amount={self._amount}"
        headers = {"apikey": api}
        response = requests.request("GET", url, headers=headers)
        status_code = response.status_code
        result = json.loads(response.text).get('result')
        return result
