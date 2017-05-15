class Deleter(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context):
        """
        Initializes attributes.

        Parameters
        ----------
        db_context : DbContext
            The database context to work with.
        """

        ### Validate parameters.
        if db_context is None:
            raise Exception('db_context cannot be None.')

        ### Attributes from outside.
        self._db_context = db_context
