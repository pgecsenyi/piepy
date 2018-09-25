from dal.deleter import Deleter

class VideoDataDeleter(Deleter):

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def delete_subtitle_path(self, subtitle_id):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get the language and the title for the specified subtitle.
            cursor.execute(
                'SELECT s.id_language, f.id_title '
                'FROM video_subtitle AS s LEFT OUTER JOIN video_file AS f ON f.id=s.id_file '
                'WHERE s.id=? '
                'LIMIT 1',
                (subtitle_id,))
            row = cursor.fetchone()
            language_id, title_id = 0, None
            if row is not None:
                language_id, title_id = row[0], row[1]

            # Delete the subtitle entry.
            cursor.execute('DELETE FROM video_subtitle WHERE id=?', (subtitle_id,))

            # If the corresponding file is not deleted from the database yet, then remove the obsolete title - subtitle
            # language mappings.
            if title_id is not None:
                self._delete_sl_mappings_recursively(cursor, title_id, language_id)

            # Commit.
            connection.commit()

    def delete_video_path(self, video_id):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get the title and the quality of the specified file as well as the number of the other children of this
            # title.
            cursor.execute(
                'SELECT v1.id_title, v1.id_quality, COUNT(v2.id_title) '
                'FROM video_file AS v1, video_file AS v2 '
                'WHERE v1.id=? AND v2.id_title=v1.id_title '
                'LIMIT 1',
                (video_id,))
            row = cursor.fetchone()
            if row is None:
                return
            title_id, missing_quality, number_of_files = row[0], row[1], row[2]

            # Get the languages to be removed from mappings.
            missing_languages = []
            cursor.execute('SELECT id_language FROM video_file_language_mapping WHERE id_file=?', (video_id,))
            rows = cursor.fetchall()
            if rows:
                missing_languages = [row[0] for row in rows]

            # Delete the specified video file and the corresponding language mappings.
            cursor.execute('DELETE FROM video_file WHERE id=?', (video_id,))
            cursor.execute('DELETE FROM video_file_language_mapping WHERE id_file=?', (video_id,))

            # If this was the only file stored for this title, we have to delete the title too.
            if number_of_files == 1:

                self._delete_title_recursively(cursor, title_id, missing_languages, missing_quality)

            else:

                # If the deleted file was the only one from this quality for this title, then remove the mapping.
                cursor.execute('SELECT id, id_quality FROM video_file WHERE id_title=?', (title_id,))
                rows = cursor.fetchall()
                if rows:
                    available_qualities = [row[1] for row in rows]
                    missing_quality = self._delete_unavailable_quality(
                        cursor, title_id, missing_quality, available_qualities)

                # If the deleted file was in a language that no other files are available in for this title, then delete
                # the corresponding mappings.
                cursor.execute(
                    'SELECT id_language FROM video_file_language_mapping WHERE id_file {}'.format(
                        self._build_in_clause([row[0] for row in rows])))
                rows = cursor.fetchall()
                if rows:
                    available_languages = [row[0] for row in rows]
                    missing_languages = self._delete_unavailable_languages(
                        cursor, title_id, missing_languages, available_languages)

                self._delete_l_q_mappings_recursively(cursor, title_id, missing_languages, missing_quality)

            # Commit.
            connection.commit()

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _build_in_clause(self, simple_list):

        return 'IN ({})'.format(','.join([str(i) for i in simple_list]))

    def _check_missing_languages(self, cursor, title_ids, missing_languages):

        cursor.execute(
            'SELECT id_language FROM video_title_language_mapping WHERE id_title {} AND id_language {} LIMIT 1'.format(
                self._build_in_clause(title_ids),
                self._build_in_clause(missing_languages)))
        rows = cursor.fetchall()
        if rows:
            available_languages = [row[0] for row in rows]
            return self._subtract_lists(missing_languages, available_languages)

        return missing_languages

    def _check_missing_quality(self, cursor, title_ids, missing_quality):

        cursor.execute(
            'SELECT id_quality FROM video_title_quality_mapping WHERE id_title {} AND id_quality=? LIMIT 1'.format(
                self._build_in_clause(title_ids)),
            missing_quality)
        row = cursor.fetchone()
        if row is None:
            return missing_quality

        return None

    def _delete_l_q_mappings_recursively(self, cursor, title_id, missing_languages, missing_quality):

        # If there are no more stuff to delete, return.
        if missing_quality is None and not missing_languages:
            return

        # Get the title's parent and siblings.
        parent_id = self._retrieve_title_parent(cursor, title_id)
        if parent_id is None:
            return
        sibling_ids = self._retrieve_title_children(cursor, parent_id)

        # Check if the parent has the removed quality from another child.
        if missing_quality is not None:
            missing_quality = self._check_missing_quality(cursor, sibling_ids, missing_quality)
            if missing_quality is not None:
                self._delete_quality_from_mapping(cursor, parent_id, missing_quality)

        # Check if the parent has the removed languages from other children.
        if missing_languages:
            missing_languages = self._check_missing_languages(cursor, sibling_ids, missing_languages)
            if missing_languages:
                self._delete_languages_from_mapping(cursor, parent_id, missing_languages)

        self._delete_l_q_mappings_recursively(cursor, parent_id, missing_languages, missing_quality)

    def _delete_languages_from_mapping(self, cursor, title_id, language_ids):

        in_clause = self._build_in_clause(language_ids)
        cursor.execute(
            'DELETE FROM video_title_language_mapping WHERE id_title=? AND id_language {}'.format(in_clause),
            (title_id,))

    def _delete_title_recursively(self, cursor, title_id, missing_languages, missing_quality):

        # If there are no more stuff to delete, return.
        if missing_quality is None and not missing_languages:
            return

        # Get the title's parent first, we may need to delete that too.
        parent_id = self._retrieve_title_parent(cursor, title_id)

        # Delete the title and the corresponding mappings.
        cursor.execute('DELETE FROM video_title WHERE id=?', (title_id,))
        cursor.execute('DELETE FROM video_title_language_mapping WHERE id_title=?', (title_id,))
        cursor.execute('DELETE FROM video_title_quality_mapping WHERE id_title=?', (title_id,))

        # Check the siblings of the title.
        if parent_id is None:
            return

        sibling_ids = self._retrieve_title_children(cursor, parent_id)

        # In case the specified title was the only child of it's parent, then remove the parent.
        if sibling_ids is None or not sibling_ids:

            self._delete_title_recursively(cursor, parent_id, missing_languages, missing_quality)

        # There are more children here, we should remove obsolete mappings only.
        else:

            missing_languages = self._check_missing_languages(cursor, sibling_ids, missing_languages)
            if missing_languages:
                self._delete_languages_from_mapping(cursor, parent_id, missing_languages)

            missing_quality = self._check_missing_quality(cursor, sibling_ids, missing_quality)
            if missing_quality is not None:
                self._delete_quality_from_mapping(cursor, parent_id, missing_quality)

            # We could just call this function in the else branch, but this way it is a bit faster (we do not repeat the
            # query for the siblings).
            self._delete_l_q_mappings_recursively(cursor, parent_id, missing_languages, missing_quality)

    def _delete_sl_mappings_recursively(self, cursor, title_id, language_id):

        # Get the title's parent.
        parent_id = self._retrieve_title_parent(cursor, title_id)

        # Delete the corresponding mapping for this title.
        cursor.execute(
            'DELETE FROM video_title_subtitle_language_mapping WHERE id_title=? AND id_language=?',
            (title_id, language_id))

        # Check the siblings of the title.
        if parent_id is None:
            return

        sibling_ids = self._retrieve_title_children(cursor, parent_id)

        # If this title is the only child, go see about it's parents.
        if sibling_ids is None or not sibling_ids:

            self._delete_sl_mappings_recursively(cursor, parent_id, language_id)

        # If there is any sibling of this title, check them.
        else:

            # Check if any of the siblings also has this language.
            in_clause = self._build_in_clause(sibling_ids)
            cursor.execute(
                'SELECT id_language FROM video_title_subtitle_language_mapping '
                'WHERE id_title {} AND id_language=?'.format(in_clause),
                (language_id,))
            rows = cursor.fetchall()

            # If no siblings are present with this language, then go to the parent and remove the mappings there too.
            if rows is None or not rows:
                self._delete_sl_mappings_recursively(cursor, parent_id, language_id)

    def _delete_quality_from_mapping(self, cursor, title_id, quality_id):

        cursor.execute(
            'DELETE FROM video_title_quality_mapping WHERE id_title=? AND id_quality=? LIMIT 1',
            (title_id, quality_id))

    def _delete_unavailable_languages(self, cursor, title_id, missing_languages, available_languages):

        missing_languages = self._subtract_lists(missing_languages, available_languages)
        if missing_languages:
            self._delete_languages_from_mapping(cursor, title_id, missing_languages)

        return missing_languages

    def _delete_unavailable_quality(self, cursor, title_id, missing_quality, available_qualities):

        if missing_quality not in available_qualities:
            self._delete_quality_from_mapping(cursor, title_id, missing_quality)
            return missing_quality

        return None

    def _retrieve_title_children(self, cursor, title_id):

        cursor.execute('SELECT id FROM video_title WHERE id_parent=?', (title_id,))
        rows = cursor.fetchall()
        if rows is None or not rows:
            return None

        return [row[0] for row in rows]

    def _retrieve_title_parent(self, cursor, title_id):

        cursor.execute('SELECT id_parent FROM video_title WHERE id=? AND id_parent IS NOT NULL LIMIT 1', (title_id,))
        row = cursor.fetchone()
        if row is None:
            return None

        return row[0]

    def _subtract_lists(self, list_a, list_b):

        return [l for l in list_a if l not in list_b]
