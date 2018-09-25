class PathFilterFactory:
    """
    An interface for building a filter stack which consists of zero or more filters. Different filter factories can be
    created for different file types.
    """

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def create_filters(self):
        """
        Creates a list of filters to be used during analyzation.

        Returns
        -------
        A list of filters.
        """
        pass
