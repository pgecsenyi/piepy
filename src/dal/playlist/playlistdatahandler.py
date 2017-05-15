from dal.playlist.entities import Playlist, PlaylistHeader, PlaylistTrack

class PlaylistDataHandler(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context):

        ### Validate parameters.
        if db_context is None:
            raise Exception('db_context cannot be None.')

        ### Attributes from outside.
        self._db_context = db_context

    ####################################################################################################################
    # Public methods.
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
                'CREATE TABLE playlist ('
                'id INTEGER PRIMARY KEY, title VARCHAR(255), time_created DATETIME)')
            cursor.execute(
                'CREATE TABLE track ('
                'id INTEGER PRIMARY KEY,'
                'id_playlist INTEGER,'
                'number INTEGER,'
                'category VARCHAR(255),'
                'title VARCHAR(1024),'
                'path VARCHAR(1024),'
                'audio_output INTEGER,'
                'FOREIGN KEY(id_playlist) REFERENCES playlist(id))')

    def delete_playlist(self, playlist_id):
        """
        Deletes the given playlist.

        Parameters
        ----------
        playlist_id : int
            The ID of the playlist to delete.
        """

        # Verify arguments.
        if playlist_id is None:
            return

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Delete the playlist with the given ID and delete it's tracks.
            cursor.execute('DELETE FROM playlist WHERE id=?', (playlist_id,))
            cursor.execute('DELETE FROM track WHERE id_playlist=?', (playlist_id,))

            # Commit.
            connection.commit()

    def delete_track(self, track_id):
        """
        Deletes the given track.

        Parameters
        ----------
        track_id : int
            The ID of the track to delete.
        """

        # Verify arguments.
        if track_id is None:
            return

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Delete the track with the given ID.
            cursor.execute('DELETE FROM track WHERE id=?', (track_id,))

            # Commit.
            connection.commit()

    def insert_playlist(self, new_playlist):
        """
        Inserts a new playlist with the given title and tracks.

        Parameters
        ----------
        new_playlist : NewPlaylist
            The playlist object to insert.

        Returns
        -------
        The ID of the inserted playlist.
        """

        # Verify arguments.
        if new_playlist is None:
            return

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the header of the playlist first, then deal with the tracks.
            cursor.execute(
                'INSERT INTO playlist (title, time_created) VALUES (?, DATETIME("now"))',
                (new_playlist.title,))
            playlist_id = cursor.lastrowid
            self._insert_tracks(cursor, playlist_id, new_playlist.tracks)

            # Commit.
            connection.commit()

            return playlist_id

    def insert_track(self, playlist_id, new_track, number_after=0):
        """
        Inserts a new track into the given playlist.

        Parameters
        ----------
        playlist_id : int
            The ID of the playlist this track belongs to.
        new_track : NewPlaylistTrack
            The track to insert.
        number_after : int
            The number of the track after which the new track has to be inserted. If set to 0, the new track will be
            inserted to the beginning of the list.

        Returns
        -------
        The ID of the inserted track.
        """

        # Verify arguments.
        if playlist_id is None or new_track is None:
            return

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Insert the new track. If no specific number was provided, make this the last track.
            number = 1
            if number_after <= 0:
                last_number = self._retrieve_last_track_number(cursor, playlist_id)
                number = last_number + 1
            else:
                cursor.execute('UPDATE track SET number=number+1 WHERE number>?', (number_after,))
                number = number_after + 1

            cursor.execute(
                'INSERT INTO track (id_playlist, number, category, title, path, audio_output) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (playlist_id, number, new_track.category, new_track.title, new_track.path, new_track.audio_output))

            track_id = cursor.lastrowid

            # Commit.
            connection.commit()

            return track_id

    def move_track(self, playlist_id, number_to_move, number_after):
        """
        Inserts a new track into the given playlist.

        Parameters
        ----------
        playlist_id : int
            The ID of the playlist this track belongs to.
        number_to_move : int
            The number of the track to move.
        number_after : int
            The number of the track after which the new track has to be moved. If set to 0, the new track will be
            inserted to the beginning of the list.
        """

        # Verify arguments.
        if playlist_id is None:
            return
        if number_to_move <= 0 or number_to_move == number_after or number_to_move == number_after + 1:
            return

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Move the track.
            if number_after < 0:
                number_after = 0
            # Get the ID of the track to move.
            cursor.execute('SELECT id FROM track WHERE number=? LIMIT 1', (number_to_move,))
            row = cursor.fetchone()
            id_to_move = row[0]
            # If we are moving a track down, then move the others up.
            if number_to_move < number_after:
                cursor.execute('UPDATE track SET number=number-1 WHERE number>?', (number_to_move,))
                # Use "number_after" instead of "number_after + 1" because the corresponding track's number has been
                # decreased by one.
                cursor.execute('UPDATE track SET number=? WHERE id=?', (number_after, id_to_move))
            # If we are moving a track up, then move the others down.
            else:
                cursor.execute('UPDATE track SET number=number+1 WHERE number>?', (number_after,))
                cursor.execute('UPDATE track SET number=? WHERE id=?', (number_after + 1, id_to_move))

            # Commit.
            connection.commit()

    def retrieve_playlist(self, playlist_id):
        """
        Retrieves the playlist with the given ID.

        Parameters
        ----------
        playlist_id : int
            The ID of the playlist to retrieve.

        Returns
        -------
        A Playlist object if there's any playlist with the given ID, otherwise None. If the playlist ID is None, then
        returns None.
        """

        # Verify arguments.
        if playlist_id is None:
            return None

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Retrieve tracks.
            tracks = self._retrieve_tracks(cursor, playlist_id)

            # Get the playlist.
            cursor.execute('SELECT title FROM playlist WHERE id=? LIMIT 1', (playlist_id,))

            # Fetch result.
            row = cursor.fetchone()
            if row is None:
                return None

            playlist = Playlist(playlist_id, row[0], tracks)

            return playlist

    def retrieve_playlist_headers(self):
        """
        Retrieves the list of all playlists from the database.

        Returns
        -------
        A list of PlaylistHeaders.
        """

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get the title of each and every playlist.
            cursor.execute('SELECT id, title FROM playlist')

            # Fetch result.
            rows = cursor.fetchall()
            if rows is None or len(rows) <= 0:
                return None
            playlist_headers = []
            for row in rows:
                playlist_headers.append(PlaylistHeader(row[0], row[1]))

            return playlist_headers

    def update_playlist(self, playlist):
        """
        Overwrites the tracks of the given playlist in the database.

        Parameters
        ----------
        playlist : Playlist
            The playlist to update.
        """

        # Verify arguments.
        if playlist is None or playlist.playlist_id is None:
            return

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Update playlist.
            cursor.execute('UPDATE playlist SET title=? WHERE id=?', (playlist.title, playlist.playlist_id))

            # Commit.
            connection.commit()

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _insert_tracks(self, cursor, playlist_id, new_tracks):
        """
        Inserts the tracks for the playlist given by it's ID into the database.

        Parameters
        ----------
        cursor : Cursor
            The cursor object for the database connection.
        playlist_id : int
            The ID of the playlist which these tracks are belong to.
        new_tracks : list of NewPlaylistTrack
            The tracks to insert.
        """

        if new_tracks is None:
            return

        for i in range(0, len(new_tracks)):
            cursor.execute(
                'INSERT INTO track (id_playlist, number, category, title, path, audio_output) '
                'VALUES (?, ?, ?, ?, ?, ?)',
                (playlist_id, i + 1, new_tracks[i].category, new_tracks[i].title, new_tracks[i].path,
                 new_tracks[i].audio_output))

    def _retrieve_last_track_number(self, cursor, playlist_id):

        cursor.execute('SELECT COUNT(*) FROM track WHERE id_playlist=?', (playlist_id,))

        row = cursor.fetchone()
        if row is None:
            return None

        return row[0]

    def _retrieve_tracks(self, cursor, playlist_id):
        """
        Retrieves the tracks of the given playlist.

        Parameters
        ----------
        cursor : Cursor
            The cursor object for the database connection.
        playlist_id : int
            The ID of the playlist to query tracks from.

        Returns
        -------
        A list of PlaylistTracks.
        """

        # Get the tracks of the playlist.
        cursor.execute(
            'SELECT id, category, title, path, audio_output FROM track WHERE id_playlist=? ORDER BY number',
            (playlist_id,))

        # Fetch result.
        rows = cursor.fetchall()
        if rows is None or len(rows) <= 0:
            return None

        tracks = []
        for row in rows:
            track = PlaylistTrack(row[0], row[1], row[2], row[3], row[4])
            tracks.append(track)

        return tracks
