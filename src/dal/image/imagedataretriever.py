from dal.functions import build_result_dictionary
from dal.retriever import Retriever

class ImageDataRetriever(Retriever):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context, cache):

        ### Call base class constructor.
        super(ImageDataRetriever, self).__init__(db_context, cache)

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def retrieve_album_id(self, album):

        album_id = self._cache.get_album_id(album)
        if album_id is None:
            album_id = self._retrieve_single_value_from_db('SELECT id FROM image_album WHERE album=? LIMIT 1', album)
            self._cache.set_album_id(album, album_id)

        return album_id

    def retrieve_albums(self):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            cursor.execute('SELECT id, album FROM image_album ORDER BY album')
            result = build_result_dictionary(cursor, ['id', 'album'])

            return result

    def retrieve_file_count(self):

        return self._retrieve_count('image_file')

    def retrieve_paths(self, album_id=None):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Build and execute the query.
            query_parameters = {}
            where_clause = ''
            if album_id != None:
                where_clause = ' WHERE id_album=:id_album'
                query_parameters['id_album'] = album_id
            cursor.execute('SELECT id, path FROM image_file' + where_clause, query_parameters)
            result = build_result_dictionary(cursor, ['id', 'path'])

            return result
