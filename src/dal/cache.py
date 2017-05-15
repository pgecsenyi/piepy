class Cache(object):

    def _get_value_from_simple_cache(self, cache, lock, key):

        with lock:
            if key in cache:
                return cache[key]

        return None

    def _store_item_in_simple_cache(self, cache, lock, key, value):

        if key != None:
            with lock:
                cache[key] = value

        return None
