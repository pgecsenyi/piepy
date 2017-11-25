from dal.functions import build_result_dictionary
from dal.retriever import Retriever

class VideoDataRetriever(Retriever):

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def retrieve_details(self, title_id):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            cursor.execute('SELECT id, title FROM video_title WHERE video_title.id=? LIMIT 1', (title_id,))
            row = cursor.fetchone()
            if row is None:
                return None

            result = {
                'id' : row[0],
                'title' : row[1],
                'files' : [],
                'subtitles' : []}

            # Get file details.
            cursor.execute(
                'SELECT f.id AS id, q.quality AS quality, l.language AS language '
                'FROM video_file AS f, video_quality AS q, video_file_language_mapping AS m '
                'INNER JOIN video_language AS l ON l.id=m.id_language '
                'WHERE f.id_title=? AND q.id=f.id_quality AND m.id_file=f.id',
                (title_id,))
            rows = cursor.fetchall()
            if rows is None or not rows:
                return None

            for row in rows:
                result['files'].append({'id' : row[0], 'language' : row[2], 'quality' : row[1]})

            # Get subtitles.
            for video_file in result['files']:

                cursor.execute(
                    'SELECT s.id, l.language '
                    'FROM video_subtitle AS s, video_language AS l '
                    'WHERE s.id_file=? AND l.id=s.id_language',
                    (video_file['id'],))
                rows = cursor.fetchall()
                if rows != None and rows:
                    for row in rows:
                        result['subtitles'].append({'file' : video_file['id'], 'id' : row[0], 'language' : row[1]})

            return result

    def retrieve_file_count(self):

        return self._retrieve_count('video_file')

    def retrieve_file_data(self, file_id):

        return self._execute_file_data_query(
            file_id,
            'SELECT f.path, t.title '
            'FROM video_file AS f, video_title AS t '
            'WHERE f.id=? AND t.id=f.id_title '
            'LIMIT 1')

    def retrieve_file_id(self, title, quality, language):

        title_id = self.retrieve_lower_title_id(title)
        language_id = self.retrieve_language_id(language)
        quality_id = self.retrieve_quality_id(quality)

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get the appropriate file's ID.
            cursor.execute(
                'SELECT f.id '
                'FROM video_file AS f, video_file_language_mapping AS m '
                'WHERE f.id_title=? AND f.id_quality=? AND m.id_language=? AND f.id=m.id_file '
                'LIMIT 1',
                (title_id, quality_id, language_id))
            row = cursor.fetchone()
            if row is None:
                return None
            file_id = row[0]

            return file_id

    def retrieve_languages(self):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            cursor.execute('SELECT id, language FROM video_language ORDER BY language')
            result = build_result_dictionary(cursor, ['id', 'language'])

            return result

    def retrieve_language_id(self, language):

        language_id = self._cache.get_language_id(language)
        if language_id is None:
            language_id = self._retrieve_single_value_from_db(
                'SELECT id FROM video_language WHERE language=? LIMIT 1',
                language)
            self._cache.set_language_id(language, language_id)

        return language_id

    def retrieve_lower_title_id(self, title):

        # Check if the given title is already available in the cache.
        title_id = self._cache.get_title_id_from_other_parents(title, 0)
        if title_id != None:
            return title_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Try to get the corresponding ID from the database.
            cursor.execute(
                'SELECT id, id_parent FROM video_title WHERE title=? AND id_parent IS NOT NULL LIMIT 1',
                (title,))
            row = cursor.fetchone()
            if row is None:
                return None
            title_id, parent_id = row

        # Store the title in the cache.
        self._cache.set_title_id(title, title_id, parent_id)

        return title_id

    def retrieve_qualities(self):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            cursor.execute('SELECT id, quality FROM video_quality ORDER BY quality')
            result = build_result_dictionary(cursor, ['id', 'quality'])

            return result

    def retrieve_quality_id(self, quality):

        quality_id = self._cache.get_quality_id(quality)
        if quality_id is None:
            quality_id = self._retrieve_single_value_from_db(
                'SELECT id FROM video_quality WHERE quality=? LIMIT 1',
                quality)
            self._cache.set_quality_id(quality, quality_id)

        return quality_id

    def retrieve_subtitle_path(self, subtitle_id):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get table contents.
            cursor.execute('SELECT path FROM video_subtitle WHERE id=? LIMIT 1', (subtitle_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            subtitle_path = row[0]

            return subtitle_path

    def retrieve_subtitle_paths(self):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Build and execute the query.
            cursor.execute('SELECT id, path FROM video_subtitle')
            result = build_result_dictionary(cursor, ['id', 'path'])

            return result

    def retrieve_title_id(self, title, parent_id=0):

        # Check if the given title is already available in the cache.
        title_id = self._cache.get_title_id(title, parent_id)
        if title_id != None:
            return title_id

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Try to get the corresponding ID from the database.
            if parent_id == 0:
                cursor.execute('SELECT id FROM video_title WHERE id_parent IS NULL AND title=? LIMIT 1', (title,))
            else:
                cursor.execute('SELECT id FROM video_title WHERE id_parent=? AND title=? LIMIT 1', (parent_id, title))
            row = cursor.fetchone()
            if row is None:
                return None
            title_id = row[0]

        # Store the title in the cache.
        self._cache.set_title_id(title, title_id, parent_id)

        return title_id

    def retrieve_titles(self, title_filter=None):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Build and execute the query.
            query_parameters = {}
            where_clause_beginning = self._build_filtering_query_start(title_filter, query_parameters)
            self._query_titles_by_filter(cursor, title_filter, where_clause_beginning, query_parameters)
            result = build_result_dictionary(cursor, ['id', 'title'])

            return result

    def retrieve_video_path(self, file_id):

        return self._retrieve_single_value_from_db('SELECT path FROM video_file WHERE id=? LIMIT 1', file_id)

    def retrieve_video_paths(self):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Build and execute the query.
            cursor.execute('SELECT id, path FROM video_file')
            result = build_result_dictionary(cursor, ['id', 'path'])

            return result

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _append_to_where_clause(self, where_clause, condition):

        if where_clause == '':
            return 'WHERE ' + condition

        return where_clause + 'AND ' + condition

    def _build_filtering_query_start(self, title_filter, query_parameters):

        where_clause_beginning = ''

        if title_filter is None:

            where_clause_beginning = 'WHERE t.id_parent IS NULL '

        else:

            if not title_filter.any_parent:
                if title_filter.parent_id is None:
                    where_clause_beginning = 'WHERE t.id_parent IS NULL '
                else:
                    where_clause_beginning = 'WHERE t.id_parent=:parent_id '
                    query_parameters['parent_id'] = title_filter.parent_id

            if title_filter.subtitle_language_id != None:
                where_clause_beginning = self._append_to_where_clause(
                    where_clause_beginning,
                    '(t.id IN (SELECT id_title ' \
                    + 'FROM video_title_subtitle_language_mapping ' \
                    + 'WHERE id_language=:subtitle_language_id)) ')
                query_parameters['subtitle_language_id'] = title_filter.subtitle_language_id

            if title_filter.text != None:
                where_clause_beginning = self._append_to_where_clause(where_clause_beginning, 'title LIKE :text ')
                query_parameters['text'] = '%' + title_filter.text + '%'

        return where_clause_beginning

    def _query_titles_by_filter(self, cursor, title_filter, where_clause_beginning, query_parameters):

        if title_filter is None or (title_filter.language_id is None and title_filter.quality_id is None):

            cursor.execute(
                'SELECT t.id, t.title FROM video_title AS t ' + where_clause_beginning + 'ORDER BY t.title',
                query_parameters)

        elif title_filter.language_id is None:

            query_parameters['quality_id'] = title_filter.quality_id
            self._query_titles_by_q(cursor, where_clause_beginning, query_parameters)

        elif title_filter.quality_id is None:

            query_parameters['language_id'] = title_filter.language_id
            self._query_titles_by_l(cursor, where_clause_beginning, query_parameters)

        else:

            query_parameters['language_id'] = title_filter.language_id
            query_parameters['quality_id'] = title_filter.quality_id
            self._query_titles_by_l_q(cursor, where_clause_beginning, query_parameters)

    def _query_titles_by_l(self, cursor, where_clause_beginning, query_parameters):
        """
        Queries titles by language.
        """

        cursor.execute(
            'SELECT t.id, t.title '
            'FROM video_title_language_mapping AS m, video_title AS t '
            + where_clause_beginning +
            'AND m.id_language=:language_id AND t.id=m.id_title '
            'GROUP BY t.title '
            'ORDER BY t.title',
            query_parameters)

    def _query_titles_by_l_q(self, cursor, where_clause_beginning, query_parameters):
        """
        Queries titles by language and quality.
        """

        cursor.execute(
            'SELECT t.id, t.title '
            'FROM video_title_language_mapping AS m1, video_title_quality_mapping AS m2, video_title AS t '
            + where_clause_beginning +
            'AND m1.id_language=:language_id AND m2.id_quality=:quality_id '
            'AND m1.id_title=m2.id_title AND t.id=m1.id_title '
            'GROUP BY t.title '
            'ORDER BY t.title',
            query_parameters)

    def _query_titles_by_q(self, cursor, where_clause_beginning, query_parameters):
        """
        Queries titles by quality.
        """

        cursor.execute(
            'SELECT t.id, t.title '
            'FROM video_title_quality_mapping AS m, video_title AS t '
            + where_clause_beginning +
            'AND m.id_quality=:quality_id AND t.id=m.id_title '
            'GROUP BY title '
            'ORDER BY title',
            query_parameters)
