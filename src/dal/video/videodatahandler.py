from dal.constants import DAL_UNCATEGORIZED
from dal.video.videodatacache import VideoDataCache
from dal.video.videodatacreator import VideoDataCreator
from dal.video.videodatadeleter import VideoDataDeleter
from dal.video.videodataretriever import VideoDataRetriever
from dal.datahandler import DataHandler

class VideoDataHandler(DataHandler):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context):

        ### Call base class constructor.
        super(VideoDataHandler, self).__init__(db_context)

        ### Private attributes.
        self._cache = VideoDataCache()
        self._retriever = VideoDataRetriever(self._db_context, self._cache)
        self._creator = VideoDataCreator(self._db_context, self._cache, self._retriever)
        self._deleter = VideoDataDeleter(self._db_context)

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def uncategorized_language_id(self):
        return self.retriever.retrieve_language_id(DAL_UNCATEGORIZED)

    @property
    def uncategorized_quality_id(self):
        return self.retriever.retrieve_quality_id(DAL_UNCATEGORIZED)

    @property
    def uncategorized_title_id(self):
        return self.retriever.retrieve_title_id(DAL_UNCATEGORIZED)

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def clear_cache(self):

        self._cache.clear()
