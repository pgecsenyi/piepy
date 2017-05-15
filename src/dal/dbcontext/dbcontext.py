import dal.context.DbConnectionManager
import dal.context.DbConnectionProvider

class DbContext(object):

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
    # Properties.
    ####################################################################################################################

    def connection_provider(self):

        return DbConnectionProvider(self._connection_manager)
