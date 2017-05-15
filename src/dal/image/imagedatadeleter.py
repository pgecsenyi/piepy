from dal.deleter import Deleter

class ImageDataDeleter(Deleter):

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def delete_path(self, file_id):

        # Connect to the database.
        with self._db_context.get_connection_provider() as connection:
            cursor = connection.cursor

            # Get the corresponding album ID and the number of tracks in that album.
            cursor.execute(
                'SELECT i1.id_album, COUNT(i2.id_album) '
                'FROM image_file AS i1, image_file AS i2 '
                'WHERE i1.id=? AND i2.id_album=i1.id_album '
                'LIMIT 1',
                (file_id,))
            row = cursor.fetchone()
            if row is None:
                return
            album_id, number_of_files = row[0], row[1]

            # Delete the specified file.
            cursor.execute('DELETE FROM image_file WHERE id=?', (file_id,))

            # If this was the only image stored for this album, we have to delete the album too.
            if number_of_files == 1:
                cursor.execute('DELETE FROM image_album WHERE id=?', (album_id,))

            # Commit.
            connection.commit()
