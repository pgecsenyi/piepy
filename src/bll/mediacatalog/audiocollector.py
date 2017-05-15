from dal.configuration.tags import TAG_ARTIST, TAG_ALBUM, TAG_NUMBER, TAG_TITLE
from indexing.collector import Collector
from indexing.functions import get_filename_without_extension

class AudioCollector(Collector):
    """
    Catalogizes audio files.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, audio_dal):

        ### Validate parameters.
        if audio_dal is None:
            raise Exception('audio_dal cannot be None.')

        ### Attributes from outside.
        self._audio_dal = audio_dal

    ####################################################################################################################
    # Collector implementation.
    ####################################################################################################################

    def collect_categorized(self, categorized_nodes):

        # Nothing to do here.
        if categorized_nodes is None or len(categorized_nodes) <= 0:
            return

        for node in categorized_nodes:
            self._store_categorized(node)

    def collect_uncategorized(self, uncategorized_nodes):

        # Nothing to do here.
        if uncategorized_nodes is None or len(uncategorized_nodes) <= 0:
            return

        for node in uncategorized_nodes:
            self._store_uncategorized(node)

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _store_categorized(self, node):

        # Insert artist, album, number and title into database.
        artist_id = self._insert_artist(node.meta)
        album_id = self._insert_album(node.meta, artist_id)
        number = self._get_number(node.meta)
        title = self._get_title(node)

        # Insert the file path.
        self._audio_dal.creator.insert_file(album_id, number, title, node.path)

    def _store_uncategorized(self, node):

        self._audio_dal.creator.insert_file(
            self._audio_dal.uncategorized_album_id,
            0,
            get_filename_without_extension(node.path),
            node.path)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _get_number(self, metadata):

        if TAG_NUMBER in metadata:
            return metadata[TAG_NUMBER]

        return 0

    def _get_title(self, node):

        if TAG_TITLE in node.meta:
            return node.meta[TAG_TITLE]

        return get_filename_without_extension(node.path)

    def _insert_album(self, metadata, artist_id):

        if TAG_ALBUM in metadata:
            return self._audio_dal.creator.insert_album(artist_id, metadata[TAG_ALBUM])

        return self._audio_dal.uncategorized_album_id

    def _insert_artist(self, metadata):

        if TAG_ARTIST in metadata:
            return self._audio_dal.creator.insert_artist(metadata[TAG_ARTIST])

        return self._audio_dal.uncategorized_artist_id
