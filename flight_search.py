import requests
import os
from dotenv import load_dotenv

load_dotenv()

IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.getenv('AMADEUS_API_KEY')
        self._api_secret = os.getenv('AMADEUS_API_SECRET')
        self._token = self.authenticate()
        self.header = {'Authorization': f'Bearer {self._token}'}

    def authenticate(self):

        auth_header = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }
        
        response = requests.post(url=TOKEN_ENDPOINT, data=body, headers=auth_header)
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token

    def obtain_iata_code(self, city):

        parameter = {'keyword': city}
        response = requests.get(url=IATA_ENDPOINT, params=parameter, headers=self.header)
        response.raise_for_status()

        try:
            code = response.json()["data"][0]['iataCode']
        except IndexError:
            print(f"IndexError: No airport code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport code found for {city}.")
            return "Not Found"

        return code

    def find_cheap_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):

        parameters = {
            'originLocationCode': origin_city_code,
            'destinationLocationCode': destination_city_code,
            'departureDate': from_time.strftime('%Y-%m-%d'),
            'returnDate': to_time.strftime('%Y-%m-%d'),
            'adults': 1,
            'nonStop': 'true' if is_direct else 'false',
            'currencyCode': 'GBP',
            'max': '10'
        }
        response = requests.get(url=FLIGHT_ENDPOINT, params=parameters, headers=self.header)
        response.raise_for_status()

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("Response body:", response.text)
            return None

        return response.json()
