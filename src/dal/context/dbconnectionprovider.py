from dal.context.dbconnectionadapter import DbConnectionAdapter

class DbConnectionProvider:

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, connection_manager, check_connection=True):

        ### Validate parameters.
        if connection_manager is None:
            raise Exception('connection_manager cannot be None.')

        ### Attributes from outside.
        self._connection_manager = connection_manager
        self._check_connection = check_connection

    ####################################################################################################################
    # Context management protocol.
    ####################################################################################################################

    def __enter__(self):

        connection = self._connection_manager.connect(self._check_connection)

        return DbConnectionAdapter(connection)

    def __exit__(self, exec_type, value, traceback):

        self._connection_manager.close()
