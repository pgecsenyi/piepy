from dal.configuration.tags import TAG_ALBUM
from indexing.collector import Collector
from indexing.functions import get_filename_without_extension

class ImageCollector(Collector):
    """
    Catalogizes image files.
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

    ####################################################################################################################
    # Collector implementation.
    ####################################################################################################################

    def collect_categorized(self, categorized_nodes):

        # Nothing to do here.
        if not categorized_nodes:
            return

        for node in categorized_nodes:
            self._store_categorized(node)

    def collect_uncategorized(self, uncategorized_nodes):

        # Nothing to do here.
        if not uncategorized_nodes:
            return

        for node in uncategorized_nodes:
            self._store_uncategorized(node)

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _store_categorized(self, node):

        album_id = self._insert_album(node.meta)
        self._image_dal.creator.insert_file(album_id, node.path)

    def _store_uncategorized(self, node):

        self._image_dal.creator.insert_file(
            self._image_dal.uncategorized_album_id,
            0,
            get_filename_without_extension(node.path),
            node.path)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _insert_album(self, metadata):

        if TAG_ALBUM in metadata:
            return self._image_dal.creator.insert_album(metadata[TAG_ALBUM])

        return self._image_dal.uncategorized_album_id
