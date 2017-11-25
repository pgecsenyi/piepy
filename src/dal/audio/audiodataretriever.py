from dal.functions import build_result_dictionary
from dal.retriever import Retriever

class AudioDataRetriever(Retriever):

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def retrieve_album_id(self, album):

        album_id = self._cache.get_album_id(album)
        if album_id is None:
            album_id = self._retrieve_single_value_from_db('SELECT id FROM audio_album WHERE album=? LIMIT 1', album)
            self._cache.set_album_id(album, album_id)

        return album_id

    def retrieve_albums(self, artist_id=None):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            where_clause = ''
            query_parameters = {}
            if artist_id != None:
                where_clause = 'WHERE id_artist=:id_artist '
                query_parameters = {'id_artist' : artist_id}
            cursor.execute('SELECT id, album FROM audio_album ' + where_clause + 'ORDER BY album', query_parameters)

            result = build_result_dictionary(cursor, ['id', 'album'])

            return result

    def retrieve_artist_id(self, artist):

        artist_id = self._cache.get_artist_id(artist)
        if artist_id is None:
            artist_id = self._retrieve_single_value_from_db(
                'SELECT id FROM audio_artist WHERE artist=? LIMIT 1',
                artist)
            self._cache.set_artist_id(artist, artist_id)

        return artist_id

    def retrieve_artists(self):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            cursor.execute('SELECT id, artist FROM audio_artist ORDER BY artist')
            result = build_result_dictionary(cursor, ['id', 'artist'])

            return result

    def retrieve_file_count(self):

        return self._retrieve_count('audio_file')

    def retrieve_file_data(self, file_id):

        return self._execute_file_data_query(file_id, 'SELECT path, title FROM audio_file WHERE id=? LIMIT 1')

    def retrieve_path(self, file_id):

        return self._retrieve_single_value_from_db('SELECT path FROM audio_file WHERE id=? LIMIT 1', file_id)

    def retrieve_paths(self):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Build and execute the query.
            cursor.execute('SELECT id, path FROM audio_file')
            result = build_result_dictionary(cursor, ['id', 'path'])

            return result

    def retrieve_tracks(self, album_id=None):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            where_clause = ''
            query_parameters = {}
            if album_id != None:
                where_clause = 'WHERE id_album=:id_album '
                query_parameters = {'id_album' : album_id}
            cursor.execute(
                'SELECT id, number, title FROM audio_file ' + where_clause + 'ORDER BY title',
                query_parameters)

            result = build_result_dictionary(cursor, ['id', 'number', 'title'])

            return result
