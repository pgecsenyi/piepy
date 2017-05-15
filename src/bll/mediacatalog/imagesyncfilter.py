from indexing.filters.pathfilter import PathFilter

class ImageSyncFilter(PathFilter):
    """
    This filter makes it possible to do an incremental synchronization instead of a full rebuild. It ignores already
    exisiting paths from the analyzation process and gathers removed files, then invokes the appropriate DAL operations
    to apply the changes.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, image_dal):

        ### Validate parameters.
        if image_dal is None:
            raise Exception('image_dal cannot be None.')

        ### Attributes from outside.
        self._image_dal = image_dal

        ### Private attributes.
        # A dictionary that stores file paths as id (int) => path (string) pairs.
        self._stored_paths = {}

    ####################################################################################################################
    # PathFilter implementation.
    ####################################################################################################################

    def apply_filter(self, path):

        for i in range(0, len(self._stored_paths)):
            if path == self._stored_paths[i]['path']:
                del self._stored_paths[i]
                return True

        return False

    def clean_filter(self):

        for id_and_path in self._stored_paths:
            self._image_dal.deleter.delete_path(id_and_path['id'])

    def init_filter(self):

        self._stored_paths = self._image_dal.retriever.retrieve_paths()

    def leave_scope(self):

        pass
