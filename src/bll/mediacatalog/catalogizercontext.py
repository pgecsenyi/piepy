class CatalogizerContext(object):
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
        self.audio_dal = None
        self.image_dal = None
        self.video_dal = None
