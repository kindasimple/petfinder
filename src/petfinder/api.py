#!/usr/bin/env python
from pathlib import Path
from typing import Optional, Union

from cachetools import TTLCache, cached
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from petfinder.client import API_KEY, API_SECRET
from petfinder.export import ApiClient, ApiClientLocalFSCache
from petfinder.types import QueryParams

app = FastAPI()
cache: TTLCache = TTLCache(maxsize=1, ttl=600)


client = ApiClient(API_SECRET, API_KEY)


@cached(cache)
def get_client(**kwargs) -> ApiClientLocalFSCache:
    client = ApiClientLocalFSCache(
        API_SECRET,
        API_KEY,
        QueryParams(**kwargs),
        cache_dir=Path("./data").as_posix(),
        archive_dir=Path("./archive").as_posix(),
        fetch=False,
    )
    return client


app.mount("/static", StaticFiles(directory="./src/static"), name="static")


@cached(cache)
def get_cached_dog_breeds(
    exclude_breeds: Optional[str] = None, include_breeds: Optional[str] = None
):
    exclude = exclude_breeds.split(",") if exclude_breeds else []
    include = set(include_breeds.split(",")) if include_breeds else set([])
    breeds = client.get_dog_breed(exclude_breeds=exclude)
    if include:
        breeds = list(filter(lambda breed: breed["name"] in include, breeds))
    return {"breeds": breeds}


@cached(cache)
def get_cached_animals(animal_type: str, breed: str, updates: Optional[bool] = False):
    client = get_client(location="San Francisco, CA", distance=10, limit=100)
    if updates:
        animals = client.updates(
            animal_type, breed, location="San Francisco, CA", distance=10, limit=100
        )
    else:
        animals = client.search(
            animal_type, breed, location="San Francisco, CA", distance=10, limit=100
        )
    return {"animals": animals}


@app.get("/types/dog/breeds/")
def get_dog_breeds(
    exclude_breeds: Union[str, None] = "", include_breeds: Union[str, None] = ""
):
    return get_cached_dog_breeds(
        exclude_breeds=exclude_breeds, include_breeds=include_breeds
    )


@app.get("/animals/")
def get_animals(animal_type: str = "dog", breed: str = "Vizsla"):
    return get_cached_animals(animal_type, breed)


@app.get("/updates/")
def get_animal_updates(animal_type: str = "dog", breed: str = "Vizsla"):
    return get_cached_animals(animal_type, breed, updates=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
