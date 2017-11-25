from dal.constants import DAL_UNCATEGORIZED
from dal.creator import Creator

class VideoDataCreator(Creator):

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
                'CREATE TABLE video_language'
                '(id INTEGER PRIMARY KEY, language VARCHAR(255))')
            cursor.execute(
                'CREATE TABLE video_quality'
                '(id INTEGER PRIMARY KEY, quality VARCHAR(255))')
            cursor.execute(
                'CREATE TABLE video_title ('
                'id INTEGER PRIMARY KEY,'
                'id_parent INTEGER,'
                'title VARCHAR(1024),'
                'FOREIGN KEY(id_parent) REFERENCES video_title(id))')
            cursor.execute(
                'CREATE TABLE video_file ('
                'id INTEGER PRIMARY KEY,'
                'id_title INTEGER,'
                'id_quality INTEGER,'
                'path VARCHAR(1024),'
                'FOREIGN KEY(id_title) REFERENCES video_title(id),'
                'FOREIGN KEY(id_quality) REFERENCES video_quality(id))')
            cursor.execute(
                'CREATE TABLE video_file_language_mapping ('
                'id INTEGER PRIMARY KEY,'
                'id_file INTEGER,'
                'id_language INTEGER,'
                'FOREIGN KEY(id_file) REFERENCES video_file(id),'
                'FOREIGN KEY(id_language) REFERENCES video_language(id))')
            cursor.execute(
                'CREATE TABLE video_subtitle ('
                'id INTEGER PRIMARY KEY,'
                'id_file INTEGER,'
                'id_language INTEGER,'
                'path VARCHAR(1024),'
                'FOREIGN KEY(id_file) REFERENCES video_file(id),'
                'FOREIGN KEY(id_language) REFERENCES video_language(id))')

            # Create auxiliary tables. These contain redundant data for kind of caching purposes, but they are actually
            # inevitable for more complex queries that filter titles by languages, qualities or subtitles. This is
            # because title parents are stored in a recursive manner and iterating through them would involve more
            # queries otherwise.
            cursor.execute(
                'CREATE TABLE video_title_language_mapping ('
                'id INTEGER PRIMARY KEY,'
                'id_title INTEGER,'
                'id_language INTEGER,'
                'FOREIGN KEY(id_title) REFERENCES video_title(id),'
                'FOREIGN KEY(id_language) REFERENCES video_language(id))')
            cursor.execute(
                'CREATE TABLE video_title_quality_mapping ('
                'id INTEGER PRIMARY KEY,'
                'id_title INTEGER,'
                'id_quality INTEGER,'
                'FOREIGN KEY(id_title) REFERENCES video_title(id),'
                'FOREIGN KEY(id_quality) REFERENCES video_quality(id))')
            cursor.execute(
                'CREATE TABLE video_title_subtitle_language_mapping ('
                'id INTEGER PRIMARY KEY,'
                'id_title INTEGER,'
                'id_language INTEGER,'
                'FOREIGN KEY(id_title) REFERENCES video_title(id),'
                'FOREIGN KEY(id_language) REFERENCES video_language(id))')

        # Fill DB with initial data.
        self._inflate_db()

    ####################################################################################################################
    # Public methods -- insert.
    ####################################################################################################################

    def insert_file(self, title_id, quality_id, path):
        """
        Inserts the given file path into database.

        Parameters
        ----------
        title_id : int
            The ID of the corresponding title.
        quality_id : int
            The ID of the corresponding quality.
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
                'INSERT INTO video_file (id_title, id_quality, path) VALUES (?, ?, ?)',
                (title_id, quality_id, path))
            path_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return path_id

    def insert_file_language_mapping(self, file_id, language_id):
        """
        Inserts the given file - language mapping into database.

        Parameters
        ----------
        file_id : int
            The ID of the file.
        language_id : int
            The ID of the language.

        Returns
        -------
        The ID of the inserted mapping.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the mapping into the database.
            cursor.execute(
                'INSERT INTO video_file_language_mapping (id_file, id_language) VALUES (?, ?)',
                (file_id, language_id))
            mapping_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return mapping_id

    def insert_language(self, language):
        """
        Inserts the given language into database and stores it and the corresponding ID in the cache. Does nothing if it
        is already stored in the database.

        Parameters
        ----------
        language : str
            The language to insert.

        Returns
        -------
        The ID of the inserted language.
        """

        # Check if the given language is already inserted.
        language_id = self._retriever.retrieve_language_id(language)
        if language_id != None:
            return language_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the language into the database.
            cursor.execute('INSERT INTO video_language (language) VALUES (?)', (language,))
            language_id = cursor.lastrowid

            # Close connection.
            connection.commit()

        # Store the language in the cache.
        self._cache.set_language_id(language, language_id)

        return language_id

    def insert_quality(self, quality):
        """
        Inserts the given quality into database and stores it and the corresponding ID in the cache. Does nothing if it
        is already stored in the database.

        Parameters
        ----------
        quality : str
            The quality to insert.

        Returns
        -------
        The ID of the inserted quality.
        """

        # Check if the given quality is already inserted.
        quality_id = self._retriever.retrieve_quality_id(quality)
        if quality_id != None:
            return quality_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the quality into the database.
            cursor.execute('INSERT INTO video_quality (quality) VALUES (?)', (quality,))
            quality_id = cursor.lastrowid

            # Commit.
            connection.commit()

        # Store the quality in the cache.
        self._cache.set_quality_id(quality, quality_id)

        return quality_id

    def insert_subtitle(self, file_id, language_id, path):
        """
        Inserts the given file path into database.

        Parameters
        ----------
        file_id : int
            The ID of the corresponding file.
        language_id : int
            The ID of the corresponding language.
        path : str
            The path to insert.

        Returns
        -------
        The ID of the inserted subtitle.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the subtitle into the database.
            cursor.execute(
                'INSERT INTO video_subtitle (id_file, id_language, path) VALUES (?, ?, ?)',
                (file_id, language_id, path))
            subtitle_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return subtitle_id

    def insert_title(self, title, parent_id=0):
        """
        Inserts the given title into database and stores it and the corresponding ID in the cache. Does nothing if it
        is already stored in the database.

        Parameters
        ----------
        title : str
            The title to insert.
        parent_id : int
            The ID of the title's parent.

        Returns
        -------
        The ID of the inserted title.
        """

        # Check if the given quality is already inserted.
        title_id = self._retriever.retrieve_title_id(title, parent_id)
        if title_id != None:
            return title_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert title into the database.
            if parent_id == 0:
                cursor.execute('INSERT INTO video_title (title) VALUES (?)', (title,))
            else:
                cursor.execute('INSERT INTO video_title (id_parent, title) VALUES (?, ?)', (parent_id, title))
            title_id = cursor.lastrowid

            # Commit.
            connection.commit()

        # Store the title in the cache.
        self._cache.set_title_id(title, title_id, parent_id)

        return title_id

    def insert_title_language_mapping(self, title_id, language_id):
        """
        Inserts the given title - language mapping into database.

        Parameters
        ----------
        title_id : int
            The ID of the title.
        language_id : int
            The ID of the language.

        Returns
        -------
        The ID of the inserted mapping.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the mapping into the database.
            cursor.execute(
                'INSERT INTO video_title_language_mapping (id_title, id_language) VALUES (?, ?)',
                (title_id, language_id))
            mapping_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return mapping_id

    def insert_title_quality_mapping(self, title_id, quality_id):
        """
        Inserts the given title - quality mapping into database.

        Parameters
        ----------
        title_id : int
            The ID of the title.
        quality_id : int
            The ID of the quality.

        Returns
        -------
        The ID of the inserted mapping.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the mapping into the database.
            cursor.execute(
                'INSERT INTO video_title_quality_mapping (id_title, id_quality) VALUES (?, ?)',
                (title_id, quality_id))
            mapping_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return mapping_id

    def insert_title_sl_mapping(self, title_id, language_id):
        """
        Inserts the given title - subtitle language mapping into database.

        Parameters
        ----------
        title_id : int
            The ID of the title.
        language_id : int
            The ID of the language.

        Returns
        -------
        The ID of the inserted mapping.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the mapping into the database.
            cursor.execute(
                'INSERT INTO video_title_subtitle_language_mapping (id_title, id_language) VALUES (?, ?)',
                (title_id, language_id))
            mapping_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return mapping_id

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

        # Insert categories into database and store the resulting IDs.
        uncategorized_language_id = self.insert_language(DAL_UNCATEGORIZED)
        uncategorized_quality_id = self.insert_quality(DAL_UNCATEGORIZED)
        uncategorized_title_id = self.insert_title(DAL_UNCATEGORIZED)

        # Insert the title - language and title - quality mappings.
        self.insert_title_language_mapping(uncategorized_title_id, uncategorized_language_id)
        self.insert_title_quality_mapping(uncategorized_title_id, uncategorized_quality_id)
