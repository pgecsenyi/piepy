import threading

from dal.cache import Cache

class ImageDataCache(Cache):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Private attributes.
        # A cache that contains albums as album (string) => id (int) pairs.
        self._album_cache = {}
        # This lock is used for album cache synchronization.
        self._album_cache_lock = threading.Lock()

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def clear(self):

        with self._album_cache_lock:
            self._album_cache = {}

    def get_album_id(self, album):

        return self._get_value_from_simple_cache(self._album_cache, self._album_cache_lock, album)

    def set_album_id(self, album, album_id):

        self._store_item_in_simple_cache(self._album_cache, self._album_cache_lock, album, album_id)
