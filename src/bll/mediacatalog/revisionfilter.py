from indexing.filters.directoryfilter import DirectoryFilter

class RevisionFilter(DirectoryFilter):
    """
    Ignores older revisions of files.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Call base class constructor.
        super(RevisionFilter, self).__init__('^[0-9]{8} [0-9]{6}$')
