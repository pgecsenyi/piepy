import threading

from dal.cache import Cache

class AudioDataCache(Cache):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Private attributes.
        # A cache that contains albums as album (string) => id (int) pairs.
        self._album_cache = {}
        # This lock is used for album cache synchronization.
        self._album_cache_lock = threading.Lock()
        # A cache that contains artist IDs as artist (string) => id (int) pairs.
        self._artist_cache = {}
        # This lock is used for artist cache synchronization.
        self._artist_cache_lock = threading.Lock()

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def clear(self):

        with self._artist_cache_lock:
            self._artist_cache = {}
        with self._album_cache_lock:
            self._album_cache = {}

    def get_album_id(self, album):

        return self._get_value_from_simple_cache(self._album_cache, self._album_cache_lock, album)

    def get_artist_id(self, artist):

        return self._get_value_from_simple_cache(self._artist_cache, self._artist_cache_lock, artist)

    def set_album_id(self, album, album_id):

        self._store_item_in_simple_cache(self._album_cache, self._album_cache_lock, album, album_id)

    def set_artist_id(self, artist, artist_id):

        self._store_item_in_simple_cache(self._artist_cache, self._artist_cache_lock, artist, artist_id)
