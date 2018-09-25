from dal.context.dbconnectionmanager import DbConnectionManager
from dal.context.dbconnectionprovider import DbConnectionProvider

class DbContext:

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, database_path):

        ### Validate parameters.
        if database_path is None:
            raise Exception('database_path cannot be None.')

        ### Attributes from outside.
        self._connection_manager = DbConnectionManager(database_path)

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def get_connection_provider(self, check_path=True):

        return DbConnectionProvider(self._connection_manager, check_path)
