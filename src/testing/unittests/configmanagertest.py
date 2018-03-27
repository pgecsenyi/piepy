"""
Config Manager unit tests.
"""

import unittest

from dal.configuration.config import Config, DatabaseConfig, IndexingConfig, LoggingConfig, MultimediaConfig, WebConfig
from dal.configuration.configmanager import ConfigManager
from testing.testhelper import TestHelper

class ConfigManagerTest(unittest.TestCase):

    ####################################################################################################################
    # Initialization and cleanup.
    ####################################################################################################################

    @classmethod
    def setUpClass(cls):

        # Create TestHelper.
        cls._helper = TestHelper()

        # Create test files.
        cls._helper.create_root_path()

    @classmethod
    def tearDownClass(cls):

        cls._helper.clean()

    ####################################################################################################################
    # Test methods.
    ####################################################################################################################

    def test_configmanager(self):

        original_config = self._create_test_config()
        ConfigManager.save(self._helper.config_path, original_config)
        ConfigManager.load(self._helper.config_path)
        loaded_config = ConfigManager.settings

        self.assertNotEqual(
            loaded_config,
            original_config,
            'The loaded config instance should not be equal to the original.')
        self._assert_configs_are_equal(
            loaded_config,
            original_config,
            'The loaded config should contain the same values as the original.')

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _assert_configs_are_equal(self, config1, config2, error_message):

        are_equal = self._check_if_configs_are_equal(config1, config2)

        self.assertTrue(are_equal, error_message)

    def _check_if_configs_are_equal(self, config1, config2):

        return config1.database.lifetime == config2.database.lifetime \
            and config1.database.path_media == config2.database.path_media \
            and config1.database.path_playlist == config2.database.path_playlist \
            and config1.indexing.audio.extensions == config2.indexing.audio.extensions \
            and config1.indexing.audio.path == config2.indexing.audio.path \
            and config1.indexing.audio.pattern == config2.indexing.audio.pattern \
            and config1.indexing.image.extensions == config2.indexing.image.extensions \
            and config1.indexing.image.path == config2.indexing.image.path \
            and config1.indexing.image.pattern == config2.indexing.image.pattern \
            and config1.indexing.video.extensions == config2.indexing.video.extensions \
            and config1.indexing.video.ignore_revisions == config2.indexing.video.ignore_revisions \
            and config1.indexing.video.path == config2.indexing.video.path \
            and config1.indexing.video.subtitle_extensions == config2.indexing.video.subtitle_extensions \
            and config1.indexing.video.subtitle_pattern == config2.indexing.video.subtitle_pattern \
            and config1.indexing.video.video_pattern == config2.indexing.video.video_pattern \
            and config1.logging.enabled == config2.logging.enabled \
            and config1.logging.level == config2.logging.level \
            and config1.logging.max_size_bytes == config2.logging.max_size_bytes \
            and config1.logging.path == config2.logging.path \
            and config1.multimedia.av_player == config2.multimedia.av_player \
            and config1.multimedia.av_player_path == config2.multimedia.av_player_path \
            and config1.multimedia.image_viewer == config2.multimedia.image_viewer \
            and config1.multimedia.image_viewer_path == config2.multimedia.image_viewer_path \
            and config1.web.port == config2.web.port

    def _create_test_config(self):

        config = Config()

        config.database = self._create_test_database_config()
        config.indexing = self._create_test_indexing_config()
        config.logging = self._create_test_logging_config()
        config.multimedia = self._create_test_multimedia_config()
        config.web = self._create_test_web_config()

        return config

    def _create_test_database_config(self):

        config = DatabaseConfig()

        config.lifetime = 4096
        config.path_media = 'test.db'
        config.path_playlist = 'test2.db'

        return config

    def _create_test_indexing_config(self):

        config = IndexingConfig()

        config.audio.extensions = ['.ext1', '.ext2']
        config.audio.path = ['/audio']
        config.audio.pattern = 'audio_pattern'
        config.image.extensions = ['.ext3', '.ext4']
        config.image.path = ['/photo']
        config.image.pattern = 'image_pattern'
        config.video.extensions = ['.ext5', '.ext6']
        config.video.ignore_revisions = False
        config.video.path = ['/video']
        config.video.subtitle_extensions = ['.ext7']
        config.video.subtitle_pattern = 'subtitle_pattern'
        config.video.video_pattern = 'video_pattern'

        return config

    def _create_test_logging_config(self):

        config = LoggingConfig()

        config.enabled = False
        config.level = 'warning'
        config.max_size_bytes = 512
        config.path = 'log'

        return config

    def _create_test_multimedia_config(self):

        config = MultimediaConfig()

        config.av_player = 'player'
        config.av_player_path = 'path_to_player'
        config.image_viewer = 'viewer'
        config.image_viewer_path = 'path_to_viewer'

        return config

    def _create_test_web_config(self):

        config = WebConfig()

        config.port = 5555

        return config

########################################################################################################################
# Main.
########################################################################################################################

if __name__ == '__main__':

    unittest.main()
