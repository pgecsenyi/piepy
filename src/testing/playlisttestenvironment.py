from testing.testenvironment import TestEnvironment

class PlaylistTestEnvironment(TestEnvironment):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, playlist_data_handler):

        ### Validate parameters.
        if playlist_data_handler is None:
            raise Exception('playlist_data_handler cannot be None.')

        ### Attributes from outside.
        self._data_handler = playlist_data_handler

    ####################################################################################################################
    # TestEnvironment implementation.
    ####################################################################################################################

    def create_database(self):

        self._data_handler.create_db()

    def get_all_fake_files(self):

        pass
