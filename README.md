# Petfinder

## Quickstart

Create a [petfinder developer account](https://www.petfinder.com/developers/signup/) and make an API key. Expose the api key and secret using the environment variables `PF_API_KEY` and `PF_API_SECRET`. Do this by creating a `.env` file.

```
# ./.env
export PF_API_KEY="..."
export PF_API_SECRET="..."
```

Run the application

```bash
# retrieve dogs 100 per breed in SFO within 100m
make update

# start the local website
make start

# view the web UI
make open
```

## Overview

Use the petfinder api to download the pets for a query and then present a web UI for fast browsing.

Breed/pet info is downloaded to `./data` as json

The local website is FastApi to serve the cached endpoints though a simple local api. The website located in `./src/static/` is also avilable through the webserver and it makes xhr requests for each breed from the local api.

TODO: Figure out why the cache id is different between the export bfb911c5 and api 3a2c5d83 for some reason.

TODO: Encode slashes in the name