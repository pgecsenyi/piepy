import threading

from dal.context.dbconnection import DbConnection

class DbConnectionManager:

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, database_path):

        ### Validate parameters.
        if database_path is None:
            raise Exception('database_path cannot be None.')

        ### Attributes from outside.
        self._database_path = database_path

        ### Private attributes.
        self._connections = {}

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def close(self):

        thread_id = threading.current_thread().ident
        if thread_id in self._connections:
            if self._connections[thread_id].close():
                del self._connections[thread_id]

    def connect(self, check_path=True):

        connection = None
        thread_id = threading.current_thread().ident

        if thread_id in self._connections:
            connection = self._connections[thread_id]
        else:
            connection = DbConnection(self._database_path)
            self._connections[thread_id] = connection

        connection.connect(check_path)

        return connection
