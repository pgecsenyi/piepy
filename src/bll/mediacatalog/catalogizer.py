from datetime import datetime
from os import path, unlink
import logging
import threading

from dal.configuration.tags import AUDIO_TAG_PATTERNS, IMAGE_TAG_PATTERNS, SUBTITLE_TAG_PATTERNS, TAG_ANY, \
                                   TAG_ANY_PATTERN, TAG_END_SEPARATOR, TAG_START_SEPARATOR, VIDEO_TAG_PATTERNS
from bll.mediacatalog.audiocollector import AudioCollector
from bll.mediacatalog.audiofilterfactory import AudioFilterFactory
from bll.mediacatalog.imagecollector import ImageCollector
from bll.mediacatalog.imagefilterfactory import ImageFilterFactory
from bll.mediacatalog.videocollector import VideoCollector
from bll.mediacatalog.videofilterfactory import VideoFilterFactory
from indexing.collectible import Collectible
from indexing.indexer import Indexer
from indexing.indexerpolicy import IndexerPolicy
from indexing.pathpatternanalyzer import PathPatternAnalyzer
from indexing.tagconfig import TagConfig

class Catalogizer(object):
    """
    Responsible for refreshing the media database either by synchronizing or completely rebuilding it.
    """

    ####################################################################################################################
    # Public constants.
    ####################################################################################################################

    STATUS_COMPLETED = 0
    STATUS_IN_PROGRESS = 1
    STATUS_NOT_RUNNING = 2
    STATUS_STARTED = 3

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, context):

        ### Validate parameters.
        if context is None:
            raise Exception('context cannot be None.')
        if context.database_config is None:
            raise Exception('database_config cannot be None.')
        if context.indexing_config is None:
            raise Exception('indexing_config cannot be None.')
        if context.media_dal is None:
            raise Exception('media_dal cannot be None.')
        if context.media_dal.audio_data_handler is None:
            raise Exception('audio_data_handler cannot be None.')
        if context.media_dal.image_data_handler is None:
            raise Exception('image_data_handler cannot be None.')
        if context.media_dal.video_data_handler is None:
            raise Exception('video_data_handler cannot be None.')

        ### Attributes from outside.
        self._database_config = context.database_config
        self._indexing_config = context.indexing_config
        self._audio_dal = context.media_dal.audio_data_handler
        self._image_dal = context.media_dal.image_data_handler
        self._video_dal = context.media_dal.video_data_handler

        ### Private attributes.
        # A boolean value that indicates whether a synchronization process is running currently.
        self._is_process_running = False
        # This lock is used to synchronize the database synchronization processes.
        self._synchronization_lock_object = threading.Lock()

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def status(self):
        if self._is_process_running:
            return Catalogizer.STATUS_IN_PROGRESS
        return Catalogizer.STATUS_NOT_RUNNING

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def rebuild_database(self):

        with self._synchronization_lock_object:
            try:
                return self._rebuild_database()
            except Exception as exception:
                logging.error('Failed to rebuild media database. %s', exception)

    def rebuild_database_async(self, callback=None):

        return self._start_async_process(self.rebuild_database, callback)

    def renew_database(self):

        with self._synchronization_lock_object:

            # Check if database exists and check whether it is recent ...
            is_rebuild_needed = False

            if not path.exists(self._database_config.path_media):
                is_rebuild_needed = True
            else:
                database_age = datetime.fromtimestamp(path.getmtime(self._database_config.path_media))
                time_since_last_update = datetime.now() - database_age
                seconds_since_last_update = int(time_since_last_update.total_seconds())
                if seconds_since_last_update > self._database_config.lifetime:
                    is_rebuild_needed = True

            # ... and if not, recreate it.
            if is_rebuild_needed is True:
                self.rebuild_database()

        return True

    def synchronize_database(self):

        with self._synchronization_lock_object:
            try:
                return self._synchronize_database()
            except Exception as exception:
                logging.error('Failed to synchronize media database. %s', exception)

    def synchronize_database_async(self, callback=None):

        return self._start_async_process(self.synchronize_database, callback)

    ####################################################################################################################
    # Private methods -- Indexing.
    ####################################################################################################################

    def _index_all_files(self):

        with self._audio_dal.db_context.get_connection_provider():
            self._index_audio_files()
        with self._image_dal.db_context.get_connection_provider():
            self._index_image_files()
        with self._video_dal.db_context.get_connection_provider():
            self._index_video_files()

    def _index_audio_files(self, sync_only=False):

        config = self._indexing_config.audio
        if config is None:
            return

        # Parse path pattern.
        path_pattern_analyzer = PathPatternAnalyzer()
        tag_config = TagConfig(TAG_START_SEPARATOR, TAG_END_SEPARATOR, (TAG_ANY, TAG_ANY_PATTERN), AUDIO_TAG_PATTERNS)
        audio_pattern = path_pattern_analyzer.parse(tag_config, config.pattern)

        # Create collector and filter factory.
        audio_collector = AudioCollector(self._audio_dal)
        audio_filter_factory = AudioFilterFactory(self._audio_dal, sync_only)

        # Define policy.
        audio_collectibles = [Collectible(config.extensions, audio_pattern)]
        audio_indexer_policy = IndexerPolicy(audio_collector, audio_collectibles, audio_filter_factory)
        audio_indexer_policy.tag_any = TAG_ANY

        # Do the indexing.
        indexer = Indexer()
        indexer.add_policy(audio_indexer_policy)
        for directory in config.path:
            indexer.add_directory(directory)
        indexer.index()

    def _index_image_files(self, sync_only=False):

        config = self._indexing_config.image
        if config is None:
            return

        # Parse path pattern.
        path_pattern_analyzer = PathPatternAnalyzer()
        tag_config = TagConfig(TAG_START_SEPARATOR, TAG_END_SEPARATOR, (TAG_ANY, TAG_ANY_PATTERN), IMAGE_TAG_PATTERNS)
        image_pattern = path_pattern_analyzer.parse(tag_config, config.pattern)

        # Create collector and filter factory.
        image_collector = ImageCollector(self._image_dal)
        image_filter_factory = ImageFilterFactory(self._image_dal, sync_only)

        # Define policy.
        image_collectibles = [Collectible(config.extensions, image_pattern)]
        image_indexer_policy = IndexerPolicy(image_collector, image_collectibles, image_filter_factory)
        image_indexer_policy.tag_any = TAG_ANY

        # Do the indexing.
        indexer = Indexer()
        indexer.add_policy(image_indexer_policy)
        for directory in config.path:
            indexer.add_directory(directory)
        indexer.index()

    def _index_video_files(self, sync_only=False):

        config = self._indexing_config.video
        if config is None:
            return

        # Parse path patterns.
        path_pattern_analyzer = PathPatternAnalyzer()
        video_tag_config = TagConfig(
            TAG_START_SEPARATOR, TAG_END_SEPARATOR, (TAG_ANY, TAG_ANY_PATTERN), VIDEO_TAG_PATTERNS)
        video_pattern = path_pattern_analyzer.parse(video_tag_config, config.video_pattern)
        subtitle_tag_config = TagConfig(
            TAG_START_SEPARATOR, TAG_END_SEPARATOR, (TAG_ANY, TAG_ANY_PATTERN), SUBTITLE_TAG_PATTERNS)
        subtitle_pattern = path_pattern_analyzer.parse(subtitle_tag_config, config.subtitle_pattern)

        # Create collector and filter factory.
        video_collector = VideoCollector(self._video_dal)
        video_filter_factory = VideoFilterFactory(self._video_dal, config.ignore_revisions, sync_only)

        # Define policy.
        collectibles = [
            Collectible(config.extensions, video_pattern, 'video'),
            Collectible(config.subtitle_extensions, subtitle_pattern, 'subtitle')]
        video_indexer_policy = IndexerPolicy(video_collector, collectibles, video_filter_factory)
        video_indexer_policy.tag_any = TAG_ANY

        # Do the indexing.
        indexer = Indexer()
        indexer.add_policy(video_indexer_policy)
        for directory in config.path:
            indexer.add_directory(directory)
        indexer.index()

    ####################################################################################################################
    # Private methods -- Database manipulation.
    ####################################################################################################################

    def _clear_caches(self):

        self._audio_dal.clear_cache()
        self._image_dal.clear_cache()
        self._video_dal.clear_cache()

    def _create_database(self):

        self._audio_dal.creator.create_db()
        self._image_dal.creator.create_db()
        self._video_dal.creator.create_db()

    def _delete_database(self):

        if path.exists(self._database_config.path_media) is True:
            unlink(self._database_config.path_media)

    def _rebuild_database(self):

        if self._is_process_running:
            return Catalogizer.STATUS_IN_PROGRESS

        self._is_process_running = True

        try:
            self._delete_database()
            self._clear_caches()
            self._create_database()
            self._index_all_files()
        finally:
            self._is_process_running = False

        return Catalogizer.STATUS_COMPLETED

    def _synchronize_database(self):

        if self._is_process_running:
            return Catalogizer.STATUS_IN_PROGRESS

        self._is_process_running = True

        try:
            self._index_audio_files(True)
            self._index_image_files(True)
            self._index_video_files(True)
        finally:
            self._is_process_running = False

        return Catalogizer.STATUS_COMPLETED

    ####################################################################################################################
    # Private methods -- Asynchronous operations.
    ####################################################################################################################

    def _execute_function(self, func, callback):

        result = func()
        if callback != None:
            callback(result)

    def _start_async_process(self, func, callback=None):

        if self._is_process_running:
            return Catalogizer.STATUS_IN_PROGRESS

        try:
            thread = threading.Thread(target=self._execute_function, args=(func, callback))
            thread.start()
        except Exception as exception:
            logging.error('Failed to execute asynchronous operation. %s', exception)

        return Catalogizer.STATUS_STARTED
