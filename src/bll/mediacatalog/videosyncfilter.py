from indexing.filters.pathfilter import PathFilter

class VideoSyncFilter(PathFilter):
    """
    This filter makes it possible to do an incremental synchronization instead of a full rebuild. It ignores already
    exisiting paths from the analyzation process and gathers removed files, then invokes the appropriate DAL operations
    to apply the changes.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, video_dal):

        ### Validate parameters.
        if video_dal is None:
            raise Exception('video_dal cannot be None.')

        ### Attributes from outside.
        self._video_dal = video_dal

        ### Private attributes.
        # A list of dictionaries storing subtitle file paths as id (int) => path (string) pairs.
        self._stored_subtitle_paths = []
        # A list of dictionaries storing video file paths as id (int) => path (string) pairs.
        self._stored_video_paths = []

    ####################################################################################################################
    # PathFilter implementation.
    ####################################################################################################################

    def apply_filter(self, path):

        if self._remove_path_from_dictionary(self._stored_subtitle_paths, path):
            return True
        if self._remove_path_from_dictionary(self._stored_video_paths, path):
            return True

        return False

    def clean_filter(self):

        for id_and_path in self._stored_video_paths:
            self._video_dal.deleter.delete_video_path(id_and_path['id'])
        for id_and_path in self._stored_subtitle_paths:
            self._video_dal.deleter.delete_subtitle_path(id_and_path['id'])

    def init_filter(self):

        self._stored_video_paths = self._video_dal.retriever.retrieve_video_paths()
        self._stored_subtitle_paths = self._video_dal.retriever.retrieve_subtitle_paths()

    def leave_scope(self):

        pass

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _remove_path_from_dictionary(self, path_list, path):

        for i in range(0, len(path_list)):
            if path == path_list[i]['path']:
                del path_list[i]
                return True

        return False
