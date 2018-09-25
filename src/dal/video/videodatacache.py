import threading

from dal.cache import Cache

class VideoDataCache(Cache):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Private attributes.
        # A cache that contains language IDs as language (string) => id (int) pairs.
        self._language_cache = {}
        # This lock is used for language cache synchronization.
        self._language_cache_lock = threading.Lock()
        # A cache that contains qualities as quality (string) => id (int) pairs.
        self._quality_cache = {}
        # This lock is used for quality cache synchronization.
        self._quality_cache_lock = threading.Lock()
        # A cache that contains titles as title (string) => id (int) pairs.
        self._title_cache = {}
        # This lock is used for title cache synchronization.
        self._title_cache_lock = threading.Lock()

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def clear(self):

        with self._language_cache_lock:
            self._language_cache = {}
        with self._quality_cache_lock:
            self._quality_cache = {}
        with self._title_cache_lock:
            self._title_cache = {}

    def get_language_id(self, language):

        return self._get_value_from_simple_cache(self._language_cache, self._language_cache_lock, language)

    def get_quality_id(self, quality):

        return self._get_value_from_simple_cache(self._quality_cache, self._quality_cache_lock, quality)

    def get_title_id(self, title, parent_id=0):

        with self._title_cache_lock:
            if (parent_id in self._title_cache) and (title in self._title_cache[parent_id]):
                return self._title_cache[parent_id][title]

        return None

    def get_title_id_from_other_parents(self, title, parent_id):

        with self._title_cache_lock:
            for parent, titles in self._title_cache.items():
                if (parent != parent_id) and (title in titles):
                    return titles[title]

        return None

    def set_language_id(self, language, language_id):

        self._store_item_in_simple_cache(self._language_cache, self._language_cache_lock, language, language_id)

    def set_quality_id(self, quality, quality_id):

        self._store_item_in_simple_cache(self._quality_cache, self._quality_cache_lock, quality, quality_id)

    def set_title_id(self, title, title_id, parent_id=0):

        if title is not None:
            with self._title_cache_lock:
                if parent_id not in self._title_cache:
                    self._title_cache[parent_id] = {}
                self._title_cache[parent_id][title] = title_id
