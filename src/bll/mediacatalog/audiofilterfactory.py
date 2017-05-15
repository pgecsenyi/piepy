from bll.mediacatalog.audiosyncfilter import AudioSyncFilter
from indexing.filters.pathfilterfactory import PathFilterFactory

class AudioFilterFactory(PathFilterFactory):
    """
    Builds audio filter stack.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, audio_dal, sync_only=False):
        """
        Initializes attributes.

        Parameters
        ----------
        audio_dal : AudioDataHandler
            A reference to the audio DAL.
        sync_only : boolean
            Indicates whether only synchronization is needed.
        """

        ### Validate parameters.
        if audio_dal is None:
            raise Exception('audio_dal cannot be None.')

        # Attributes from outside.
        self._audio_dal = audio_dal
        self._sync_only = sync_only

    ####################################################################################################################
    # PathFilterFactory implementation.
    ####################################################################################################################

    def create_filters(self):

        filters = []
        if self._sync_only:
            filters.append(AudioSyncFilter(self._audio_dal))

        return filters
