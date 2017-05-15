from bll.mediacatalog.imagesyncfilter import ImageSyncFilter
from indexing.filters.pathfilterfactory import PathFilterFactory

class ImageFilterFactory(PathFilterFactory):
    """
    Builds image filter stack.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, image_dal, sync_only=False):
        """
        Initializes attributes.

        Parameters
        ----------
        image_dal : ImageDataHandler
            A reference to the image DAL.
        sync_only : boolean
            Indicates whether only synchronization is needed.
        """

        # Attributes from outside.
        self._image_dal = image_dal
        self._sync_only = sync_only

    ####################################################################################################################
    # PathFilterFactory implementation.
    ####################################################################################################################

    def create_filters(self):

        filters = []
        if self._sync_only:
            filters.append(ImageSyncFilter(self._image_dal))

        return filters
