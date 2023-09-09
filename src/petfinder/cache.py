import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from petfinder.types import QueryParams


class Archive:
    """
    Get archive api data from local file system"""

    ANIMALS_CACHE_FILENAME = "animals.json"
    DOG_BREEDS_CACHE_FILENAME = "breeds.json"

    def __init__(self, archive_dir: str):
        self._archive_dir = Path(archive_dir)

    @property
    def current_cache_dir(self):
        return self._archive_dir / datetime.now().strftime("%Y_%m_%d")

    def _get_archive_file(self, cache_filepath: str) -> List[Dict[str, Any]]:
        # If archive dir exists, list archive folders
        if self._archive_dir.exists():
            archive_folders = sorted(
                [f for f in self._archive_dir.iterdir() if f.is_dir()]
            )

            # Get cache data filepath from second to last archive folder
            cache_data_filepath = archive_folders[-2] / cache_filepath
            if cache_data_filepath.is_file():
                # If cache data filepath exists, load cache data from file
                with open(cache_data_filepath, "r", encoding="utf8") as f:
                    return json.loads(f.read())
        return []

    def archive(self, src: str):
        """Archive api data to local file system"""
        # copy files from data/cache_id to current_cache_dir
        shutil.move(src, self.current_cache_dir)


class Cache:
    """Cache data to local file system in the data folder"""

    ANIMALS_CACHE_FILENAME = "animals.json"
    DOG_BREEDS_CACHE_FILENAME = "breeds.json"

    def __init__(self, cache_dir: str, query: QueryParams):
        """Initialize cache directory"""
        self._cache_dir = Path(cache_dir)
        self.cache_id = self.get_query_hash(**query.dict())

    @property
    def cache_dir(self):
        return self._cache_dir / self.cache_id

    def _get_cache_file(self, cache_filepath: str) -> List[Dict[str, Any]]:
        """Get data from cache file"""
        if self._cache_dir.exists():
            cache_data_filepath = self.cache_dir / cache_filepath
            if cache_data_filepath.is_file():
                with open(cache_data_filepath, "r", encoding="utf8") as fh:
                    return json.loads(fh.read())
            else:
                print(f"Cache file {cache_data_filepath} does not exist")
        else:
            print(f"Cache directory {self._cache_dir} does not exist")
        return []

    def _save_cache_file(self, cache_filepath: str, data: List[Dict[str, Any]]) -> None:
        """"""
        if self.cache_dir.exists():
            self.cache_dir.mkdir(
                parents=True, exist_ok=True
            )  # create directory if not exist

        # create cache data directory if not exist
        cache_data_filepath = self.cache_dir / cache_filepath
        cache_folder = cache_data_filepath.parent
        if not cache_folder.exists():
            cache_folder.mkdir(parents=True, exist_ok=True)

        # save data to cache file
        with open(cache_data_filepath, "w", encoding="utf8") as fh:
            fh.write(json.dumps(data))

    @staticmethod
    def get_query_hash(*args, **kwargs) -> str:
        """Generate unique id for query"""
        kwargs_str = json.dumps(sorted(kwargs))
        unique_id = hashlib.sha256(f"{args},{kwargs_str}".encode("utf-8")).hexdigest()
        return unique_id[:8]
