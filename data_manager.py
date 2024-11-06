import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETY_API_ENDPOINT_PRICES = 'https://api.sheety.co/2b327fad9c4cbe0419c4e756a0757ae4/flightPrices/prices'
SHEETY_API_ENDPOINT_USERS = 'https://api.sheety.co/2b327fad9c4cbe0419c4e756a0757ae4/flightPrices/users'


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheety_bearer_token = os.getenv('SHEETY_BEARER_TOKEN')
        self.sheety_headers = {'Authorization': f'Bearer {self.sheety_bearer_token}'}

    def update_row_from_prices(self, row_id, field, value):
        body = {'prices': {f'{field}': f'{value}', }}
        response = requests.put(url=f'{SHEETY_API_ENDPOINT_PRICES}/{row_id}', json=body, headers=self.sheety_headers)
        response.raise_for_status()

    def get_rows_from_prices(self):
        response = requests.get(url=SHEETY_API_ENDPOINT_PRICES, headers=self.sheety_headers)
        response.raise_for_status()
        data = response.json()['prices']
        return data

    def get_rows_from_users(self):
        response = requests.get(url=SHEETY_API_ENDPOINT_USERS, headers=self.sheety_headers)
        response.raise_for_status()
        data = response.json()['users']
        return data
