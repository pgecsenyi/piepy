class Creator(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context, cache, retriever):
        """
        Initializes attributes.

        Parameters
        ----------
        db_context : DbContext
            The database context to work with.
        cache : Cache
            The cache for storing data inserted in the database.
        retriever : Retriever
            The object used to retrieve data.
        """

        ### Validate parameters.
        if db_context is None:
            raise Exception('db_context cannot be None.')
        if cache is None:
            raise Exception('cache cannot be None.')
        if retriever is None:
            raise Exception('retriever cannot be None.')

        ### Attributes from outside.
        self._db_context = db_context
        self._cache = cache
        self._retriever = retriever
