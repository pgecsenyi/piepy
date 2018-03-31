"""
ConfigManager

Logic for managing application configuration.
"""

import json
import os

from dal.configuration.config import Config

class ConfigManager(object):
    """
    Handles and persists application configuration.
    """

    ####################################################################################################################
    # Public static attributes.
    ####################################################################################################################

    categories = []

    settings = None

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    @staticmethod
    def load(config_file_path):
        """
        Loads settings from the given file.

        Parameters
        ----------
        config_file_path : str
            The path of the configuration file to load the settings from.
        """

        if not os.path.exists(config_file_path):
            raise Exception('The configuration file ({0}) does not exist.'.format(config_file_path))

        try:
            json_config = ''
            with open(config_file_path, 'r') as config_file:
                json_config = json.load(config_file)

            ConfigManager.settings = ConfigManager._parse_json_config(json_config)
        except KeyError as missing_key:
            raise Exception('Cannot parse configuration file, key {} is missing.'.format(missing_key))
        except Exception as exception:
            raise Exception('Cannot parse configuration file. {}'.format(exception))

    @staticmethod
    def save(config_file_path, config=None):
        """
        Stores the given configuration in the given file. If no configuration settings are given, then it uses the
        defaults stored in this class.

        Parameters
        ----------
        config_file_path : str
            The path of the configuration file to write.
        cofnig : Config
            The configuration settings to save.
        """

        if config is None:
            config = ConfigManager.settings

        try:
            json_config = ConfigManager._create_json_config(config)

            with open(config_file_path, 'w') as config_file:
                json.dump(json_config, config_file, indent=2, sort_keys=True)
        except Exception as exception:
            raise Exception('Cannot save configuration file. {}'.format(exception))

    ####################################################################################################################
    # Private methods -- Load and save.
    ####################################################################################################################

    @staticmethod
    def _create_json_config(config):
        """
        Converts the configuration to a plain Python object using dictionaries and built-in structures.

        Parameters
        ----------
        config : Config
            The configuration to save.

        Returns
        -------
        A plain Python object that can be used for JSON serialization.
        """

        json_config = {}

        # Database.
        json_config['database'] = {}
        json_config['database']['lifetime'] = config.database.lifetime
        json_config['database']['path_media'] = config.database.path_media
        json_config['database']['path_playlist'] = config.database.path_playlist

        # Indexing.
        json_config['indexing'] = {}

        json_config['indexing']['audio'] = {}
        json_config['indexing']['audio']['extensions'] = config.indexing.audio.extensions
        json_config['indexing']['audio']['paths'] = config.indexing.audio.path
        json_config['indexing']['audio']['pattern'] = config.indexing.audio.pattern

        json_config['indexing']['image'] = {}
        json_config['indexing']['image']['extensions'] = config.indexing.image.extensions
        json_config['indexing']['image']['paths'] = config.indexing.image.path
        json_config['indexing']['image']['pattern'] = config.indexing.image.pattern

        json_config['indexing']['video'] = {}
        json_config['indexing']['video']['ignore_revisions'] = config.indexing.video.ignore_revisions
        json_config['indexing']['video']['paths'] = config.indexing.video.path
        json_config['indexing']['video']['subtitle_extensions'] = config.indexing.video.subtitle_extensions
        json_config['indexing']['video']['subtitle_pattern'] = config.indexing.video.subtitle_pattern
        json_config['indexing']['video']['video_extensions'] = config.indexing.video.extensions
        json_config['indexing']['video']['video_pattern'] = config.indexing.video.video_pattern

        # Logging.
        json_config['logging'] = {}
        json_config['logging']['enabled'] = config.logging.enabled
        json_config['logging']['level'] = config.logging.level
        json_config['logging']['max_size_bytes'] = config.logging.max_size_bytes
        json_config['logging']['path'] = config.logging.path

        # Multimedia.
        json_config['multimedia'] = {}
        json_config['multimedia']['av_player'] = config.multimedia.av_player
        json_config['multimedia']['av_player_path'] = config.multimedia.av_player_path
        json_config['multimedia']['image_viewer'] = config.multimedia.image_viewer
        json_config['multimedia']['image_viewer_path'] = config.multimedia.image_viewer_path

        # Web.
        json_config['web'] = {}
        json_config['web']['port'] = config.web.port

        return json_config

    @staticmethod
    def _parse_json_config(json_config):
        """
        Creates a Config object from a plain Python object.

        Parameters
        ----------
        json_config : object
            The configuration containing the settings.

        Returns
        -------
        A Config object.
        """

        config = Config()

        # Database.
        config.database.lifetime = json_config['database']['lifetime']
        config.database.path_media = json_config['database']['path_media']
        config.database.path_playlist = json_config['database']['path_playlist']

        # Indexing.
        if 'indexing' in json_config:

            if 'audio' in json_config['indexing']:

                config.indexing.audio.extensions = json_config['indexing']['audio']['extensions']
                config.indexing.audio.path = json_config['indexing']['audio']['paths']
                config.indexing.audio.pattern = json_config['indexing']['audio']['pattern']

                ConfigManager.categories.append('audio')

            if 'image' in json_config['indexing']:

                config.indexing.image.extensions = json_config['indexing']['image']['extensions']
                config.indexing.image.path = json_config['indexing']['image']['paths']
                config.indexing.image.pattern = json_config['indexing']['image']['pattern']

                ConfigManager.categories.append('image')

            if 'video' in json_config['indexing']:

                config.indexing.video.ignore_revisions = json_config['indexing']['video']['ignore_revisions']
                config.indexing.video.extensions = json_config['indexing']['video']['video_extensions']
                config.indexing.video.path = json_config['indexing']['video']['paths']
                config.indexing.video.subtitle_extensions = json_config['indexing']['video']['subtitle_extensions']
                config.indexing.video.subtitle_pattern = json_config['indexing']['video']['subtitle_pattern']
                config.indexing.video.video_pattern = json_config['indexing']['video']['video_pattern']

                ConfigManager.categories.append('video')

        # Logging.
        if 'logging' in json_config:

            config.logging.enabled = json_config['logging']['enabled']
            config.logging.level = json_config['logging']['level']
            config.logging.max_size_bytes = json_config['logging']['max_size_bytes']
            config.logging.path = json_config['logging']['path']

        # Multimedia.
        config.multimedia.av_player = json_config['multimedia']['av_player']
        config.multimedia.av_player_path = json_config['multimedia']['av_player_path']
        config.multimedia.image_viewer = json_config['multimedia']['image_viewer']
        config.multimedia.image_viewer_path = json_config['multimedia']['image_viewer_path']

        # Web.
        config.web.port = json_config['web']['port']

        return config
