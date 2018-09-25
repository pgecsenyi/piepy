import os
import threading

class UserDataManager:
    """
    Responsible for managing user data (for example playlists database creation).
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        self._lock_object = threading.Lock()

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def create_playlist_storage(self, playlist_manager, playlist_database_path):

        with self._lock_object:
            if not os.path.exists(playlist_database_path):
                playlist_manager.create_db()
