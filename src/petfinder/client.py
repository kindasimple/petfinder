import requests
from urllib.parse import urljoin
from typing import List, Dict
import os

print(os.getenv("PF_API_KEY"))

API_KEY = os.getenv("PF_API_KEY")
API_SECRET = os.getenv("PF_API_SECRET")

# API_KEY = ""
# API_SECRET = ""


class ApiClient:

    _api_url = 'https://api.petfinder.com/v2/'
    _token_route = 'oauth2/token'
    _animal_route = 'animals'
    _type_dog_breed = 'types/dog/breeds'

    def __init__(self, api_secret: str = API_SECRET, api_key: str = API_KEY) -> None:
        self._api_secret = api_secret
        self._api_key = api_key

        if not api_secret or not api_key:
            print("API key and secret are required")
            return

        response = requests.post(
            urljoin(self._api_url, self._token_route),
            json={"grant_type": "client_credentials", "client_id": self._api_key, "client_secret": self._api_secret})

        self._token = response.json()['access_token']

        self._session = requests.Session()
        self._session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self._token}'
        })

    def search(self, animal_type: str, breed: str, location: str, distance: int = 10, limit: int = 100) -> dict:
        """
        Search for animals available for adoption
        :param animal_type: The type of animal to search for
        :param location: The location to search for
        :param distance: The distance from the location to search for
        :param limit: The maximum number of results to return
        :return: A dictionary of results
        """
        response = self._session.get(
            urljoin(self._api_url, self._animal_route),
            params={
                'type': animal_type,
                'breed': breed,
                'location': location,
                'distance': distance,
                'limit': limit
            }
        )
        return response.json()["animals"]

    def get_dog_breed(self, exclude_breeds: List[str]) -> List[Dict]:
        """
        Get a list of all dogs of a certain breed
        :param breed: The breed to search for
        :return: A dictionary of results
        """
        params = {}
        if exclude_breeds:
            params['exclude_breeds'] = ",".join(exclude_breeds)
        response = self._session.get(
            urljoin(self._api_url, self._type_dog_breed),
            params=params
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()["breeds"]
