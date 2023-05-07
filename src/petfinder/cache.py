import json
import hashlib
from pathlib import Path


class Cache:
    ANIMALS_CACHE_FILENAME = "animals.json"
    DOG_BREEDS_CACHE_FILENAME = "breeds.json"

    def __init__(self, cache_dir: str):
        self._cache_dir = Path(cache_dir)

    def _get_cache_file(self, cache_filepath: str, cache_id: str = "") -> Path:
        if self._cache_dir.exists():
            cache_data_filepath = self._cache_dir / cache_id / cache_filepath
            if cache_data_filepath.is_file():
                with open(cache_data_filepath, "r", encoding="utf8") as f:
                    return json.loads(f.read())

    def _save_cache_file(self, cache_filepath: str, data: dict, cache_id: str = "") -> None:
        # create cache directory if not exist
        cache_dir = self._cache_dir / cache_id
        if cache_dir.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)  # create directory if not exist

        # create cache data directory if not exist
        cache_data_filepath = cache_dir / cache_filepath
        cache_folder = cache_data_filepath.parent
        if not cache_folder.exists():
            cache_folder.mkdir(parents=True, exist_ok=True)

        # save data to cache file
        with open(cache_data_filepath, "w") as f:
            f.write(json.dumps(data))

    @staticmethod
    def get_query_hash(*args, **kwargs) -> str:
        kwargs_str = json.dumps(sorted(kwargs))
        unique_id = hashlib.sha256(f"{args},{kwargs_str}".encode("utf-8")).hexdigest()
        return unique_id[:8]