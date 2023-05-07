#!/usr/bin/env python
from pathlib import Path
from typing import List, Union

from cachetools import TTLCache, cached
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from petfinder.client import API_KEY, API_SECRET
from petfinder.export import ApiClientLocalFSCache


app = FastAPI()
cache = TTLCache(maxsize=1, ttl=600)
client = ApiClientLocalFSCache(API_SECRET, API_KEY, cache_dir=Path("./data"), fetch=False)

app.mount("/static", StaticFiles(directory="./src/static"), name="static")

@cached(cache)
def get_cached_dog_breeds(exclude_breeds: str = None):
    breeds = client.get_dog_breed(exclude_breeds=exclude_breeds.split(","))
    return {"breeds": breeds}

@cached(cache)
def get_cached_animals(animal_type: str = None, breed: str = None):
    animals = client.search(animal_type, breed, location="San Francisco, CA", distance=10, limit=100)
    return {"animals": animals}


@app.get('/types/dog/breeds/')
def get_dog_breeds(exclude_breeds: Union[str, None] = ''):
    return get_cached_dog_breeds(exclude_breeds=exclude_breeds)


@app.get('/animals/')
def get_animals(animal_type: str = "dog", breed: str = "Vizsla"):
    return get_cached_animals(animal_type, breed)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
