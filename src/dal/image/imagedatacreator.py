from dal.constants import DAL_UNCATEGORIZED
from dal.creator import Creator

class ImageDataCreator(Creator):

    ####################################################################################################################
    # Public methods -- create.
    ####################################################################################################################

    def create_db(self):
        """
        Creates database and tables.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider(False) as connection:
            cursor = connection.cursor

            # Create tables.
            cursor.execute(
                'CREATE TABLE image_album ('
                'id INTEGER PRIMARY KEY, album VARCHAR(255))')
            cursor.execute(
                'CREATE TABLE image_file ('
                'id INTEGER PRIMARY KEY,'
                'id_album INTEGER,'
                'path VARCHAR(1024),'
                'FOREIGN KEY(id_album) REFERENCES image_album(id))')

        # Fill DB with initial data.
        self._inflate_db()

    ####################################################################################################################
    # Public methods -- insert.
    ####################################################################################################################

    def insert_album(self, album):
        """
        Inserts the given album into database and stores it and the corresponding ID in the cache. Does nothing if it
        is already stored in the database.

        Parameters
        ----------
        album : str
            The album to insert.

        Returns
        -------
        The ID of the inserted album.
        """

        # Check if the given album is already inserted.
        album_id = self._retriever.retrieve_album_id(album)
        if album_id != None:
            return album_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the album into the database.
            cursor.execute('INSERT INTO image_album (album) VALUES (?)', (album,))
            album_id = cursor.lastrowid

            # Commit.
            connection.commit()

        # Store the album in the cache.
        self._cache.set_album_id(album, album_id)

        return album_id

    def insert_file(self, album_id, path):
        """
        Inserts the given file path into database.

        Parameters
        ----------
        album_id : int
            The ID of the corresponding album.
        path : str
            The path to insert.

        Returns
        -------
        The ID of the inserted file.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the file into the database.
            cursor.execute('INSERT INTO image_file (id_album, path) VALUES (?, ?)', (album_id, path))
            path_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return path_id

    ####################################################################################################################
    # Auxiliary methods -- initialize.
    ####################################################################################################################

    def _inflate_db(self):
        """
        Initializes the database (and assumes that it is empty).
        """

        self._insert_uncategorized_values()

    def _insert_uncategorized_values(self):
        """
        Inserts 'Uncategorized' entries in the database, we may need them later.
        """

        self.insert_album(DAL_UNCATEGORIZED)
