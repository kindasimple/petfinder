#!/usr/bin/env python3
"""
./petfinder/export.py --exclude "English Bulldog" search

python -m petfinder.export --exclude "English Bulldog" search
"""
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional

from petfinder.cache import Archive, Cache, QueryParams
from petfinder.client import API_KEY, API_SECRET, ApiClient

DEFAULT_LOCATION = "San Francisco, CA"
DEFAULT_DISTANCE = 10
DEFAULT_LIMIT = 100

DATA_PATH = Path("./data")
ARCHIVE_PATH = Path("./archive")


class ApiClientLocalFSCache(Archive, Cache, ApiClient):
    def __init__(
        self,
        api_secret: Optional[str],
        api_key: Optional[str],
        query: QueryParams,
        cache_dir: str = DATA_PATH.as_posix(),
        archive_dir: str = ARCHIVE_PATH.as_posix(),
        fetch: bool = True,
    ) -> None:
        if not api_secret or not api_key:
            raise RuntimeError("API key and secret are required")
        if cache_dir:
            Cache.__init__(self, cache_dir, query)
        if archive_dir:
            Archive.__init__(self, archive_dir)
        if api_secret and api_key:
            ApiClient.__init__(self, api_secret, api_key)
        self._fetch = fetch

    def get_dog_breed(self, exclude_breeds: List[str]) -> list:
        cache_breed_file = self.DOG_BREEDS_CACHE_FILENAME

        disallowed_breeds = [] if exclude_breeds is None else exclude_breeds

        # get cached data
        breeds_cache_data = self._get_cache_file(cache_breed_file)

        def filter_fn(breed):
            return breed["name"] not in disallowed_breeds

        if breeds_cache_data:
            return list(filter(filter_fn, breeds_cache_data))

        if not self._fetch:
            return []

        # request data from api
        breeds_data = super().get_dog_breed(disallowed_breeds)
        self._save_cache_file(self.DOG_BREEDS_CACHE_FILENAME, breeds_data)
        return list(filter(filter_fn, breeds_data))

    def search(
        self, animal_type: str, breed: str, *args, **kwargs
    ) -> List[Dict[str, Any]]:
        cache_breed_file = (
            Path(animal_type) / breed.replace("/", "") / self.ANIMALS_CACHE_FILENAME
        )
        self.get_query_hash(*args, **kwargs)
        animals = self._get_cache_file(str(cache_breed_file))
        if animals is not None:
            return animals

        if not self._fetch:
            return []

        # request data from api
        animals = super().search(animal_type, breed, *args, **kwargs)
        self._save_cache_file(cache_breed_file, animals)
        return animals

    def updates(
        self, animal_type: str, breed: str, *args, **kwargs
    ) -> List[Dict[str, Any]]:
        cache_breed_file = (
            Path(animal_type) / breed.replace("/", "") / self.ANIMALS_CACHE_FILENAME
        )
        animals = self._get_cache_file(str(cache_breed_file))

        # get archive file
        archived_animals = self._get_archive_file(str(cache_breed_file))
        seen_animal_set = (
            set(map(lambda animal: animal["id"], archived_animals))
            if archived_animals
            else set()
        )
        if animals is not None:
            # return animals
            return list(
                filter(lambda animal: animal["id"] not in seen_animal_set, animals)
            )

        if not self._fetch:
            return []

        # request data from api
        animals = super().search(animal_type, breed, *args, **kwargs)
        self._save_cache_file(str(cache_breed_file), animals)


def main(query: QueryParams, action: str, exclude_breeds: List[str]):
    if action == "hash":
        print(
            ApiClientLocalFSCache.get_query_hash(
                location=query.location, distance=query.distance, limit=query.limit
            )
        )
    elif action == "search":
        client = ApiClientLocalFSCache(API_SECRET, API_KEY, query, DATA_PATH.as_posix())
        query_hash = ApiClientLocalFSCache.get_query_hash(
            location=query.location, distance=query.distance, limit=query.limit
        )
        # remove symlink if exists
        try:
            Path(DATA_PATH / query_hash).unlink(missing_ok=True)
        except PermissionError:
            print(
                f"PermissionError: Unable to remove symlink {DATA_PATH / query_hash}."
            )

        if not client.current_cache_dir.exists():
            # the archived cache might not exist, but might have cached the data locally
            # in ./data
            breeds = client.get_dog_breed(exclude_breeds=exclude_breeds)
            for breed_dict in breeds:
                dogs = client.search(
                    "dog",
                    breed_dict["name"],
                    location=query.location,
                    distance=query.distance,
                    limit=query.limit,
                )
                print(f"{breed_dict['name']}: {len(dogs)}")
            # archive data
            print(f"archive data from {client.cache_dir} to {client.current_cache_dir}")
            client.archive(client.cache_dir)
            # client.current_cache_dir.mkdir(parents=True)
        else:
            print(
                f"Cache directory {client.current_cache_dir} already exists in archive."
                "Skipping search."
            )

        # create symlink to archive folder
        Path(DATA_PATH / query_hash).symlink_to(
            client.current_cache_dir.resolve(), target_is_directory=True
        )


if __name__ == "__main__":

    exclude_breeds = ["Husky"]

    parser = argparse.ArgumentParser(
        prog="petfinder", description="cache petfinder data"
    )
    parser.add_argument("action", choices=["search", "hash"], default="search")
    parser.add_argument("--exclude", action="append", default=exclude_breeds)
    parser.add_argument("--location", default=DEFAULT_LOCATION)
    parser.add_argument("--distance", type=int, default=DEFAULT_DISTANCE)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)

    args = parser.parse_args()
    exclude_breeds = args.exclude
    action = args.action
    query = QueryParams(
        location=args.location, distance=args.distance, limit=args.limit
    )

    print(f"Running petfinder action {action} with params: {args}")
    main(query, action, exclude_breeds)
