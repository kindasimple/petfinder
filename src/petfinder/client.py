import os
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import requests

API_KEY = os.getenv("PF_API_KEY")
API_SECRET = os.getenv("PF_API_SECRET")


class ApiClient:

    _api_url = "https://api.petfinder.com/v2/"
    _token_route = "oauth2/token"
    _animal_route = "animals"
    _type_dog_breed = "types/dog/breeds"

    def __init__(
        self, api_secret: Optional[str] = API_SECRET, api_key: Optional[str] = API_KEY
    ) -> None:

        if not api_secret or not api_key:
            raise RuntimeError("API key and secret are required")

        self._api_secret = api_secret
        self._api_key = api_key

        if not api_secret or not api_key:
            print("API key and secret are required")
            return

        request_url = urljoin(self._api_url, self._token_route)
        request_json = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        response = requests.post(
            request_url,
            json=request_json,
            timeout=30,
        )
        self._token = response.json()["access_token"]
        self._session = requests.Session()
        header_dict = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
        self._session.headers.update(header_dict)

    def search(
        self,
        animal_type: str,
        breed: str,
        location: str,
        distance: int = 10,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Search for animals available for adoption
        :param animal_type: The type of animal to search for
        :param location: The location to search for
        :param distance: The distance from the location to search for
        :param limit: The maximum number of results to return
        :return: A dictionary of results
        """
        params: Dict[str, Union[str, int]] = {
            "type": animal_type,
            "breed": breed,
            "location": location,
            "distance": distance,
            "limit": limit,
        }
        response = self._session.get(
            urljoin(self._api_url, self._animal_route),
            params=params,
        )
        return response.json()["animals"]

    def get_dog_breed(self, exclude_breeds: List[str]) -> List[Dict]:
        """
        Get a list of all dogs of a certain breed

        :param exclude_breeds: A list of breeds to exclude from the results.
        :return: A list of dictionaries containing information about the breeds.
        :raises HTTPError: If the request fails.
        """
        params = {}
        if exclude_breeds:
            params["exclude_breeds"] = ",".join(exclude_breeds)
        response = self._session.get(
            urljoin(self._api_url, self._type_dog_breed), params=params
        )
        if not response.ok:
            response.raise_for_status()
        return response.json()["breeds"]
