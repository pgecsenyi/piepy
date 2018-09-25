class StrRange:
    """
    Stores the beginning and the ending of a range in a string.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, start=0, end=0):
        """
        Initializes the attributes.

        Parameters
        ----------
        start : int
            The start index of the range.
        end : int
            The end index of the range.
        """

        ### Attributes from outside.
        self._start = start
        self._end = end

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def end(self):
        """
        Gets the end position of the range.
        """
        return self._end

    @end.setter
    def end(self, value):
        """
        Sets the end position of the range.
        """
        self._end = value

    @property
    def length(self):
        """
        Gets the length of the range.
        """
        return self._end - self._start

    @property
    def start(self):
        """
        Gets the start position of the range.
        """
        return self._start

    @start.setter
    def start(self, value):
        """
        Sets the start position of the range.
        """
        self._start = value
