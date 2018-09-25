class PathFilter:
    """
    Interface that defines how a path filter should look like. Path filters are used by the PathAnalyzer which uses
    them to decide whether a path should be analyzed (and catalogized) or not.
    """

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def apply_filter(self, path):
        """
        Applies the filter on the given path.

        Returns
        -------
        True if the given path should not be analyzed, else false.
        """
        pass

    def clean_filter(self):
        """
        Cleans the filter. This is some kind of destructor and provides filters the ability of doing something at the
        end of the analyzation process.
        """
        pass

    def init_filter(self):
        """
        Initializes the filter.
        """
        pass

    def leave_scope(self):
        """
        Indicates that the directory we are currently in is changing (we are going down or up the tree).
        """
        pass
