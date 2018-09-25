from dal.configuration.tags import TAG_EPISODE_TITLE, TAG_LANGUAGE, TAG_LANGUAGES, TAG_QUALITY, TAG_TITLE
from dal.constants import DAL_UNCATEGORIZED
from indexing.collector import Collector
from indexing.functions import get_filename_without_extension

class VideoCollector(Collector):
    """
    Catalogizes video and subtitle files.
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

    ####################################################################################################################
    # Collector implementation.
    ####################################################################################################################

    def collect_categorized(self, categorized_nodes):

        # Nothing to do here.
        if not categorized_nodes:
            return

        # Choose the appropriate action by examining the token. Process videos first so their IDs will be available when
        # catalogizing subtitles.
        for node in categorized_nodes:
            if node.token == 'video':
                self._store_categorized_video(node)

        for node in categorized_nodes:
            if node.token == 'subtitle':
                self._store_categorized_subtitle(node)

    def collect_uncategorized(self, uncategorized_nodes):

        # Nothing to do here.
        if not uncategorized_nodes:
            return

        # Choose the appropriate action by examining the token.
        for node in uncategorized_nodes:
            if node.token == 'video':
                self._store_uncategorized_video(node)

    ####################################################################################################################
    # Methods for storing categorized and uncategorized files.
    ####################################################################################################################

    def _store_categorized_subtitle(self, node):

        subtitle_language_id = self._insert_language(node.meta)
        subtitle_quality = self._get_quality(node.meta)
        episode_title = self._get_episode_title(node.meta)
        episode_title_id = self._video_dal.retriever.retrieve_lower_title_id(episode_title)
        video_languages = self._get_languages(node.meta)

        for language in video_languages:

            file_id = self._video_dal.retriever.retrieve_file_id(episode_title, subtitle_quality, language)
            if file_id is None:
                continue
            else:
                self._video_dal.creator.insert_subtitle(file_id, subtitle_language_id, node.path)
                title_id = self._get_title_id(node.meta)
                self._video_dal.creator.insert_title_sl_mapping(title_id, subtitle_language_id)
                if episode_title_id is not None:
                    self._video_dal.creator.insert_title_sl_mapping(episode_title_id, subtitle_language_id)

    def _store_categorized_video(self, node):

        # Insert languages, quality and title into database.
        language_ids = self._insert_languages(node.meta)
        quality_id = self._insert_quality(node.meta)
        title_id = self._insert_title(node.meta)

        # Insert title for the current file.
        episode_title_id = self._insert_episode_title(node.meta, title_id)

        # Insert the file path.
        file_id = self._video_dal.creator.insert_file(episode_title_id, quality_id, node.path)

        # Insert file - language and title - language mappings.
        for language_id in language_ids:
            self._video_dal.creator.insert_file_language_mapping(file_id, language_id)
            self._video_dal.creator.insert_title_language_mapping(title_id, language_id)
            self._video_dal.creator.insert_title_language_mapping(episode_title_id, language_id)

        # Insert title - quality mappings.
        self._video_dal.creator.insert_title_quality_mapping(title_id, quality_id)
        self._video_dal.creator.insert_title_quality_mapping(episode_title_id, quality_id)

    def _store_uncategorized_video(self, node):

        # Insert titles.
        parent_id = self._insert_uncategorized_parents(node.parent)
        title_id = self._video_dal.creator.insert_title(get_filename_without_extension(node.path), parent_id)

        # Insert the file path and the file - language mapping.
        file_id = self._video_dal.creator.insert_file(title_id, self._video_dal.uncategorized_quality_id, node.path)
        self._video_dal.creator.insert_file_language_mapping(file_id, self._video_dal.uncategorized_language_id)

        # Insert the title - language and title - quality mappings.
        self._video_dal.creator.insert_title_language_mapping(title_id, self._video_dal.uncategorized_language_id)
        self._video_dal.creator.insert_title_quality_mapping(title_id, self._video_dal.uncategorized_quality_id)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _get_episode_title(self, metadata):

        if TAG_EPISODE_TITLE in metadata:
            return metadata[TAG_EPISODE_TITLE]

        return self._video_dal.uncategorized_title_id

    def _get_languages(self, metadata):

        if TAG_LANGUAGES in metadata:
            return [s.strip() for s in metadata[TAG_LANGUAGES].split(',')]

        return [DAL_UNCATEGORIZED]

    def _get_quality(self, metadata):

        if TAG_QUALITY in metadata:
            return metadata[TAG_QUALITY]

        return DAL_UNCATEGORIZED

    def _get_title_id(self, metadata):

        if TAG_TITLE in metadata:
            return self._video_dal.retriever.retrieve_title_id(metadata[TAG_TITLE])

        return self._video_dal.uncategorized_title_id

    def _insert_episode_title(self, metadata, title_id):

        if TAG_EPISODE_TITLE in metadata:
            episode_title_id = self._video_dal.creator.insert_title(metadata[TAG_EPISODE_TITLE], title_id)
            return episode_title_id

        return self._video_dal.uncategorized_title_id

    def _insert_language(self, metadata):

        if TAG_LANGUAGE in metadata:
            return self._video_dal.creator.insert_language(metadata[TAG_LANGUAGE])

        return self._video_dal.uncategorized_language_id

    def _insert_languages(self, metadata):

        if TAG_LANGUAGES not in metadata:
            return [self._video_dal.uncategorized_language_id]

        language_ids = set()
        languages = [s.strip() for s in metadata[TAG_LANGUAGES].split(',')]
        for language in languages:
            language_ids.add(self._video_dal.creator.insert_language(language))

        return language_ids

    def _insert_quality(self, metadata):

        if TAG_QUALITY in metadata:
            return self._video_dal.creator.insert_quality(metadata[TAG_QUALITY])

        return self._video_dal.uncategorized_quality_id

    def _insert_title(self, metadata):

        if TAG_TITLE in metadata:
            return self._video_dal.creator.insert_title(metadata[TAG_TITLE])

        return self._video_dal.uncategorized_title_id

    def _insert_uncategorized_parents(self, uncategorized_file):
        """
        Inserts the parents of the given uorganized file into database by iterating through the them in a reverse manner
        from bottom to top recursively. Stores inserted IDs in each node and stops if a record is already inserted.

        Parameters
        ----------
        uncategorized_file : UncategorizedNode
            The uncategorized file node to insert.

        Returns
        -------
        The ID of the inserted record.
        """

        # If the given file does already have an ID (so it is stored in the database), return that.
        if uncategorized_file.id_in_database != -1:
            return uncategorized_file.id_in_database

        # If the given file does not have a parent, we will use root (which is the 'Unknown' title actually).
        if uncategorized_file.parent is None:
            parent_id = self._video_dal.uncategorized_title_id
        # If the given file has a parent, insert that first.
        else:
            parent_id = self._insert_uncategorized_parents(uncategorized_file.parent)

        # Insert the given title into the database and store the resulting ID.
        uncategorized_file.id_in_database = self._video_dal.creator.insert_title(uncategorized_file.path, parent_id)

        # Insert the title - language and title - quality mappings.
        uncategorized_language_id = self._video_dal.uncategorized_language_id
        self._video_dal.creator.insert_title_language_mapping(
            uncategorized_file.id_in_database,
            uncategorized_language_id)
        uncategorized_quality_id = self._video_dal.uncategorized_quality_id
        self._video_dal.creator.insert_title_quality_mapping(
            uncategorized_file.id_in_database,
            uncategorized_quality_id)

        return uncategorized_file.id_in_database
