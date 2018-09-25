class TagConfig:
    """
    Defines the tags used during indexing.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, start, end, tag_any, tag_patterns):
        """
        Initializes the attributes.

        Parameters
        ----------
        start : str
            The first character (start separator) of each tag.
        end : str
            The last character (end separator) of each tag.
        tag_any : tuple of str
            The name and the pattern of the any tag that can match anything in the path.
        tag_patterns : dict
            Defines the other tags and their format.
        """

        ### Validate parameters.
        if start is None:
            raise Exception('start cannot be None.')
        if end is None:
            raise Exception('end cannot be None.')
        if not tag_patterns:
            raise Exception('patterns cannot be None or empty.')

        ### Attributes from outside.
        self._start = start
        self._end = end
        self._tag_any = tag_any
        self._tag_patterns = tag_patterns

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def end(self):
        """
        Gets the end separator of each tag.
        """
        return self._end

    @property
    def start(self):
        """
        Gets the start separator of each tag.
        """
        return self._start

    @property
    def tag_any(self):
        """
        Gets the format of the ANY tag.
        """
        return self._tag_any

    @property
    def tag_patterns(self):
        """
        Gets the other tags and their format.
        """
        return self._tag_patterns
