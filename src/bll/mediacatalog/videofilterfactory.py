from bll.mediacatalog.revisionfilter import RevisionFilter
from bll.mediacatalog.videosyncfilter import VideoSyncFilter
from indexing.filters.pathfilterfactory import PathFilterFactory

class VideoFilterFactory(PathFilterFactory):
    """
    Builds video filter stack.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, video_dal, ignore_revisions=False, sync_only=False):
        """
        Initializes attributes.

        Parameters
        ----------
        video_dal : VideoDataHandler
            A reference to the video DAL.
        ignore_revisions : boolean
            Sets whether to ignore revisions.
        sync_only : boolean
            Indicates whether only synchronization is needed.
        """

        ### Validate parameters.
        if video_dal is None:
            raise Exception('video_dal cannot be None.')

        ### Attributes from outside.
        self._video_dal = video_dal
        self._ignore_revisions = ignore_revisions
        self._sync_only = sync_only

    ####################################################################################################################
    # PathFilterFactory implementation.
    ####################################################################################################################

    def create_filters(self):

        filters = []
        if self._ignore_revisions:
            filters.append(RevisionFilter())
        if self._sync_only:
            filters.append(VideoSyncFilter(self._video_dal))

        return filters
