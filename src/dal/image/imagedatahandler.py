from dal.image.imagedatacache import ImageDataCache
from dal.image.imagedatacreator import ImageDataCreator
from dal.image.imagedatadeleter import ImageDataDeleter
from dal.image.imagedataretriever import ImageDataRetriever
from dal.constants import DAL_UNCATEGORIZED
from dal.datahandler import DataHandler

class ImageDataHandler(DataHandler):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context):

        ### Call base class constructor.
        super(ImageDataHandler, self).__init__(db_context)

        ### Private attributes.
        self._cache = ImageDataCache()
        self._retriever = ImageDataRetriever(self._db_context, self._cache)
        self._creator = ImageDataCreator(self._db_context, self._cache, self._retriever)
        self._deleter = ImageDataDeleter(self._db_context)

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def uncategorized_album_id(self):
        return self.retriever.retrieve_album_id(DAL_UNCATEGORIZED)

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def clear_cache(self):

        self._cache.clear()
