from requests import post

from config import settings


class Payment:
    def __init__(self):
        self.merchant_id = settings.PAYMENT['MERCHANT']
        self.callback_url = settings.PAYMENT['CALLBACK_URL']

    def _send_request(self, url, data):
        response = post(
            url=url,
            data={
                'merchant_id': self.merchant_id,
                'callback_url': self.callback_url,
                **data
            }
        )
        return response.json()

    def payment_request(self, amount, description, mobile=None, email=None):
        if settings.PAYMENT.get('TEST'):
            url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'
        else:
            url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
        data = {
            'amount': amount,
            'description': description,
            'mobile': mobile,
            'email': email,
        }
        return self._send_request(url=url, data=data)

    def verify_payment(self, amount, authority):
        if settings.PAYMENT.get('TEST'):
            url = 'https://sandbox.zarinpal.com/pg/v4/payment/verify.json'
        else:
            url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
        data = {
            'amount': amount,
            'authority': authority
        }
        return self._send_request(url=url, data=data)
