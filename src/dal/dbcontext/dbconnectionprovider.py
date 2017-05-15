import dal.context.DbConnectionAdapter

class DbConnectionProvider(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, connection_manager):

        ### Validate parameters.
        if connection_manager is None:
            raise Exception('connection_manager cannot be None.')

        ### Attributes from outside.
        self._connection_manager = connection_manager

    ####################################################################################################################
    # Context guard methods.
    ####################################################################################################################

    def __enter__(self):

        connection = self._connection_manager.connect()

        return DbConnectionAdapter(connection)

    def __exit__(self, type, value, traceback):

        self._connection_manager.close()
