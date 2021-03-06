class Retriever:

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context, cache):
        """
        Initializes attributes.

        Parameters
        ----------
        db_context : DbContext
            The database context to work with.
        cache : Cache
            The cache for storing data retrieved from the database.
        """

        ### Attributes from outside.
        self._db_context = db_context
        self._cache = cache

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _execute_file_data_query(self, file_id, query):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            cursor.execute(query, (file_id,))
            row = cursor.fetchone()
            if row is None:
                return None, None

            # Fetch result.
            title, path = row[1], row[0]

            return title, path


    def _retrieve_count(self, table_name):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Build and execute the query.
            cursor.execute('SELECT COUNT(*) FROM ' + table_name)
            rows = cursor.fetchall()
            if not rows:
                return None
            result = rows[0][0]

            return result

    def _retrieve_single_value_from_db(self, query, value):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Try to get the corresponding ID from the database.
            cursor.execute(query, (value,))
            row = cursor.fetchone()
            if row is None:
                return None
            value_id = row[0]

            return value_id
