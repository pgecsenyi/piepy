import os
import sqlite3

class DbConnection:

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
        self._connection = None
        self._is_commit_needed = False
        self._transaction_depth = 0

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def cursor(self):
        if self._connection is None:
            return None
        return self._connection.cursor()

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def close(self):

        if (self._transaction_depth <= 1) and (self._connection is not None):
            if self._is_commit_needed:
                self._connection.commit()
            self._connection.close()
            self._connection = None
            self._is_commit_needed = False

        self._transaction_depth = self._transaction_depth - 1

        return self._connection is None

    def commit(self, do_immediately=False):

        if do_immediately:
            self._connection.commit()
        else:
            self._is_commit_needed = True

    def connect(self, check_path):

        if self._connection is None:
            if check_path:
                self._assert_db_exists()
            self._connection = sqlite3.connect(self._database_path)

        self._transaction_depth = self._transaction_depth + 1

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _assert_db_exists(self):

        if self._database_path is None or not os.path.isfile(self._database_path):
            raise Exception('Invalid database path: ' + self._database_path + '.')
