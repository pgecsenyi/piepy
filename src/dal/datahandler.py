class DataHandler:

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context):

        ### Validate parameters.
        if db_context is None:
            raise Exception('db_context cannot be None.')

        ### Attributes from outside.
        self._db_context = db_context

        ### Protected attributes.
        self._cache = None
        self._creator = None
        self._deleter = None
        self._retriever = None

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def creator(self):
        return self._creator

    @property
    def db_context(self):
        return self._db_context

    @property
    def deleter(self):
        return self._deleter

    @property
    def retriever(self):
        return self._retriever

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def clear_cache(self):

        self._cache.clear()
