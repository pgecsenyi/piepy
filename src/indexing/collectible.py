class Collectible:
    """
    Encapsulates a category to be catalogized: it's extensions, patterns and optionally a token for the Collector.
    The latter allows a Collector to process and combine data from different file types.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, extensions, path_pattern, token=None):
        """
        Constructor. Initializes attributes and checks the maximum depth provided.

        Parameters
        ----------
        extensions : list of str
            The list of the extensions for this category.
        path_pattern : PathPattern
            The pattern that describes the file paths belonging to this category.
        token : str
            An identifier forwarded to the Collector.
        """

        ### Validate parameters.
        if not extensions:
            raise Exception('extensions cannot be None or empty.')
        if path_pattern is None:
            raise Exception('path_pattern cannot be None.')

        ### Private attributes.
        self._extensions = extensions
        self._path_pattern = path_pattern
        self._token = token

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def extensions(self):
        """
        Gets the list of extensions for this category.
        """
        return self._extensions

    @property
    def path_pattern(self):
        """
        Gets the pattern that describes the file paths belonging to this category.
        """
        return self._path_pattern

    @property
    def token(self):
        """
        Gets the identifier meant to be used by the Collector.
        """
        return self._token
