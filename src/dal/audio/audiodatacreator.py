from dal.constants import DAL_UNCATEGORIZED
from dal.creator import Creator

class AudioDataCreator(Creator):

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
                'CREATE TABLE audio_artist ('
                'id INTEGER PRIMARY KEY, artist VARCHAR(1024))')
            cursor.execute(
                'CREATE TABLE audio_album ('
                'id INTEGER PRIMARY KEY,'
                'id_artist INTEGER,'
                'album VARCHAR(1024),'
                'FOREIGN KEY(id_artist) REFERENCES audio_artist(id))')
            cursor.execute(
                'CREATE TABLE audio_file ('
                'id INTEGER PRIMARY KEY,'
                'id_album INTEGER,'
                'number INTEGER,'
                'title VARCHAR(1024),'
                'path VARCHAR(1024),'
                'FOREIGN KEY(id_album) REFERENCES audio_album(id))')

        # Fill DB with initial data.
        self._inflate_db()

    ####################################################################################################################
    # Public methods -- insert.
    ####################################################################################################################

    def insert_album(self, artist_id, album):
        """
        Inserts the given album into database and stores it and the corresponding ID in the cache. Does nothing if it
        is already stored in the database.

        Parameters
        ----------
        artist_id : int
            The ID of the artist.
        album : str
            The album to insert.

        Returns
        -------
        The ID of the inserted album.
        """

        # Check if the given album is already inserted.
        album_id = self._retriever.retrieve_album_id(album)
        if album_id is not None:
            return album_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the album into the database.
            cursor.execute('INSERT INTO audio_album (id_artist, album) VALUES (?, ?)', (artist_id, album))
            album_id = cursor.lastrowid

            # Commit.
            connection.commit()

        # Store the album in the cache.
        self._cache.set_album_id(album, album_id)

        return album_id

    def insert_artist(self, artist):
        """
        Inserts the given artist into database and stores it and the corresponding ID in the cache. Does nothing if it
        is already stored in the database.

        Parameters
        ----------
        artist : str
            The artist to insert.

        Returns
        -------
        The ID of the inserted artist.
        """

        # Check if the given artist is already inserted.
        artist_id = self._retriever.retrieve_artist_id(artist)
        if artist_id is not None:
            return artist_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the artist into the database.
            cursor.execute('INSERT INTO audio_artist (artist) VALUES (?)', (artist,))
            artist_id = cursor.lastrowid

            # Commit.
            connection.commit()

        # Store the artist in the cache.
        self._cache.set_artist_id(artist, artist_id)

        return artist_id

    def insert_file(self, album_id, number, title, path):
        """
        Inserts the given file path into database.

        Parameters
        ----------
        album_id : int
            The ID of the corresponding album.
        number : int
            The number of the track in the album.
        title : str
            The title of the track.
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
            cursor.execute(
                'INSERT INTO audio_file (id_album, number, title, path) VALUES (?, ?, ?, ?)',
                (album_id, number, title, path))
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

        uncategorized_artist_id = self.insert_artist(DAL_UNCATEGORIZED)
        self.insert_album(uncategorized_artist_id, DAL_UNCATEGORIZED)
