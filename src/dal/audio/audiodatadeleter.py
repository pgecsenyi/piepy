from dal.deleter import Deleter

class AudioDataDeleter(Deleter):

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def delete_path(self, file_id):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get the corresponding album ID and the number of tracks in that album.
            cursor.execute(
                'SELECT a1.id_album, COUNT(a2.id_album) '
                'FROM audio_file AS a1, audio_file AS a2 '
                'WHERE a1.id=? AND a2.id_album=a1.id_album '
                'LIMIT 1',
                (file_id,))
            row = cursor.fetchone()
            if row is None:
                return
            album_id, number_of_tracks = row[0], row[1]

            # Delete the specified track.
            cursor.execute('DELETE FROM audio_file WHERE id=?', (file_id,))

            # If this was the only track stored for this album, we have to delete the album too.
            if number_of_tracks == 1:

                # Get the corresponding artist ID and the number of albums of that artist.
                cursor.execute(
                    'SELECT a1.id_artist, COUNT(a2.id_artist) '
                    'FROM audio_album AS a1, audio_album AS a2 '
                    'WHERE a1.id=? AND a2.id_artist=a1.id_artist '
                    'LIMIT 1',
                    (album_id,))
                row = cursor.fetchone()
                if row is None:
                    return
                artist_id, number_of_albums = row[0], row[1]

                # Delete the album.
                cursor.execute('DELETE FROM audio_album WHERE id=?', (album_id,))

                # If this was the only album stored for this artist, we have to delete the artist too.
                if number_of_albums == 1:
                    cursor.execute('DELETE FROM audio_artist WHERE id=?', (artist_id,))

            # Commit.
            connection.commit()
