from dal.audio.audiodatacache import AudioDataCache
from dal.audio.audiodatacreator import AudioDataCreator
from dal.audio.audiodatadeleter import AudioDataDeleter
from dal.audio.audiodataretriever import AudioDataRetriever
from dal.constants import DAL_UNCATEGORIZED
from dal.datahandler import DataHandler

class AudioDataHandler(DataHandler):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context):

        ### Call base class constructor.
        super(AudioDataHandler, self).__init__(db_context)

        ### Private attributes.
        self._cache = AudioDataCache()
        self._retriever = AudioDataRetriever(self._db_context, self._cache)
        self._creator = AudioDataCreator(self._db_context, self._cache, self._retriever)
        self._deleter = AudioDataDeleter(self._db_context)

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def uncategorized_album_id(self):
        return self.retriever.retrieve_album_id(DAL_UNCATEGORIZED)

    @property
    def uncategorized_artist_id(self):
        return self.retriever.retrieve_artist_id(DAL_UNCATEGORIZED)

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def clear_cache(self):

        self._cache.clear()
