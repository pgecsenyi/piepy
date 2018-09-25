class CatalogizerContext:
    """
    Stores parameters for the Catalogizer.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Private attributes.
        self.database_config = None
        self.indexing_config = None
        self.media_dal = None
