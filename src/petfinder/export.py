#!/usr/bin/env python3
"""
./petfinder/export.py --exclude "English Bulldog" search

python -m petfinder.export --exclude "English Bulldog" search
"""
from typing import List
from pathlib import Path
import sys
import argparse

# add the project directory to the sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))

from petfinder.client import ApiClient, API_KEY, API_SECRET
from petfinder.cache import Cache


class ApiClientLocalFSCache(Cache, ApiClient):
    def __init__(self, api_secret: str, api_key: str, cache_dir: Path = Path("./data"), fetch: bool = True) -> None:
        if cache_dir:
            Cache.__init__(self, cache_dir)
        if api_secret and api_key:
            ApiClient.__init__(self, api_secret, api_key)
        self._fetch = fetch

    def get_dog_breed(self, exclude_breeds: List[str]) -> list:
        cache_breed_file = self.DOG_BREEDS_CACHE_FILENAME

        if exclude_breeds is None:
            exclude_breeds = []

        # get cached data
        breeds = self._get_cache_file(cache_breed_file)

        def filter_fn(breed):
            return breed['name'] not in exclude_breeds

        if breeds:
            return list(filter(filter_fn, breeds))

        if not self._fetch:
            return []

        # request data from api
        breeds = super().get_dog_breed(exclude_breeds)
        self._save_cache_file(self.DOG_BREEDS_CACHE_FILENAME, breeds)
        return list(filter(filter_fn, breeds))

    def search(self, animal_type: str, breed: str, *args, **kwargs) -> list:
        cache_breed_file = Path(animal_type) / breed.replace("/", "") / self.ANIMALS_CACHE_FILENAME
        cache_id = self.get_query_hash(*args, **kwargs)
        animals = self._get_cache_file(cache_breed_file, cache_id=cache_id)
        if animals is not None:
            return animals

        if not self._fetch:
            return []

        # request data from api
        animals = super().search(animal_type, breed, *args, **kwargs)
        self._save_cache_file(cache_breed_file, animals, cache_id=cache_id)
        return animals


if __name__ == "__main__":

    data_path = Path("./data")
    exclude_breeds = ["Husky"]
    location = "San Francisco, CA"
    distance = 10
    limit = 100

    parser = argparse.ArgumentParser(
        prog='petfinder',
        description='cache petfinder data'
    )
    parser.add_argument('action', choices=['search', 'hash'], default='search')
    parser.add_argument('--exclude', action='append', default=exclude_breeds)
    parser.add_argument('--location', default=location)
    parser.add_argument('--distance', type=int, default=distance)
    parser.add_argument('--limit', type=int, default=distance)

    args = parser.parse_args()
    exclude_breeds = args.exclude
    location = args.location
    distance = args.distance
    limit = args.limit
    action = args.action

    print(f"Running petfinder action {action} with params: {args}")

    if action == "hash":
        print(ApiClientLocalFSCache.get_query_hash(location, distance, limit))
    elif action == "search":
        client = ApiClientLocalFSCache(API_SECRET, API_KEY, data_path)
        breeds = client.get_dog_breed(exclude_breeds=exclude_breeds)
        for breed_dict in breeds:
            dogs = client.search("dog", breed_dict["name"], location, distance, limit)
            print(f"{breed_dict['name']}: {len(dogs)}")
