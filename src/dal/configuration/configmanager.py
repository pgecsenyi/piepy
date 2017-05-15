"""
ConfigManager

Logic for managing application configuration.
"""

import configparser
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

        # Check if the given file exists.
        if not os.path.exists(config_file_path):
            raise Exception('The configuration file ({0}) does not exist.'.format(config_file_path))

        # Parse the configuration file.
        config_parser = configparser.RawConfigParser()
        config_parser.read(config_file_path)

        # Load settings.
        ConfigManager.settings = ConfigManager._load_config_from_parser(config_parser)

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

        # Instantiate configuration parser.
        config_parser = configparser.RawConfigParser()

        # Set values.
        ConfigManager._save_config_to_parser(config_parser, config)

        # Store settings.
        with open(config_file_path, 'w') as config_file:
            config_parser.write(config_file)

    ####################################################################################################################
    # Private methods -- Load and save.
    ####################################################################################################################

    @staticmethod
    def _load_config_from_parser(config_parser):
        """
        Creates a Config object and inflates it from the given ConfigParser.

        Parameters
        ----------
        config_parser : ConfigParser
            The configuration parser used to read the settings.

        Returns
        -------
        A Config object.
        """

        config = Config()

        # Database.
        config.database.lifetime = config_parser.getint('database', 'lifetime')
        config.database.path_media = config_parser.get('database', 'path_media')
        config.database.path_playlist = config_parser.get('database', 'path_playlist')

        # Indexing.
        if config_parser.has_section('indexing_audio'):

            config.indexing.audio.extensions = config_parser.get('indexing_audio', 'extensions').split(',')
            config.indexing.audio.path = ConfigManager._list_from_string(config_parser.get('indexing_audio', 'path'))
            config.indexing.audio.pattern = config_parser.get('indexing_audio', 'pattern')

            ConfigManager.categories.append('audio')

        if config_parser.has_section('indexing_image'):

            config.indexing.image.extensions = config_parser.get('indexing_image', 'extensions').split(',')
            config.indexing.image.path = ConfigManager._list_from_string(config_parser.get('indexing_image', 'path'))
            config.indexing.image.pattern = config_parser.get('indexing_image', 'pattern')

            ConfigManager.categories.append('image')

        if config_parser.has_section('indexing_video'):

            config.indexing.video.ignore_revisions = config_parser.getboolean('indexing_video', 'ignore_revisions')
            config.indexing.video.extensions = config_parser.get('indexing_video', 'video_extensions').split(',')
            config.indexing.video.path = ConfigManager._list_from_string(config_parser.get('indexing_video', 'path'))
            config.indexing.video.subtitle_extensions = config_parser \
                .get('indexing_video', 'subtitle_extensions') \
                .split(',')
            config.indexing.video.subtitle_pattern = config_parser.get('indexing_video', 'subtitle_pattern')
            config.indexing.video.video_pattern = config_parser.get('indexing_video', 'video_pattern')

            ConfigManager.categories.append('video')

        # Logging.
        if config_parser.has_section('logging'):

            config.logging.enabled = config_parser.getboolean('logging', 'enabled')
            config.logging.level = config_parser.get('logging', 'level')
            config.logging.max_size_bytes = config_parser.getint('logging', 'max_size_bytes')
            config.logging.path = config_parser.get('logging', 'path')

        # Multimedia.
        config.multimedia.av_player = config_parser.get('multimedia', 'av_player')
        config.multimedia.av_player_path = config_parser.get('multimedia', 'av_player_path')
        config.multimedia.image_viewer = config_parser.get('multimedia', 'image_viewer')
        config.multimedia.image_viewer_path = config_parser.get('multimedia', 'image_viewer_path')

        # Web.
        config.web.port = config_parser.getint('web', 'port')

        return config

    @staticmethod
    def _save_config_to_parser(config_parser, config):
        """
        Saves configuration to the given ConfigParser.

        Parameters
        ----------
        config_parser : ConfigParser
            The configuration parser used to store the settings.
        config : Config
            The configuration to save.
        """

        # Database.
        config_parser.add_section('database')
        config_parser.set('database', 'lifetime', str(config.database.lifetime))
        config_parser.set('database', 'path_media', config.database.path_media)
        config_parser.set('database', 'path_playlist', config.database.path_playlist)

        # Indexing.
        config_parser.add_section('indexing_audio')
        config_parser.set('indexing_audio', 'extensions', ','.join(config.indexing.audio.extensions))
        config_parser.set('indexing_audio', 'path', ConfigManager._list_to_string(config.indexing.audio.path))
        config_parser.set('indexing_audio', 'pattern', config.indexing.audio.pattern)

        config_parser.add_section('indexing_image')
        config_parser.set('indexing_image', 'extensions', ','.join(config.indexing.image.extensions))
        config_parser.set('indexing_image', 'path', ConfigManager._list_to_string(config.indexing.image.path))
        config_parser.set('indexing_image', 'pattern', config.indexing.image.pattern)

        config_parser.add_section('indexing_video')
        config_parser.set('indexing_video', 'ignore_revisions', config.indexing.video.ignore_revisions)
        config_parser.set('indexing_video', 'path', ConfigManager._list_to_string(config.indexing.video.path))
        config_parser.set('indexing_video', 'subtitle_extensions', ','.join(config.indexing.video.subtitle_extensions))
        config_parser.set('indexing_video', 'subtitle_pattern', config.indexing.video.subtitle_pattern)
        config_parser.set('indexing_video', 'video_extensions', ','.join(config.indexing.video.extensions))
        config_parser.set('indexing_video', 'video_pattern', config.indexing.video.video_pattern)

        # Logging.
        config_parser.add_section('logging')
        config_parser.set('logging', 'enabled', config.logging.enabled)
        config_parser.set('logging', 'level', config.logging.level)
        config_parser.set('logging', 'max_size_bytes', config.logging.max_size_bytes)
        config_parser.set('logging', 'path', config.logging.path)

        # Multimedia.
        config_parser.add_section('multimedia')
        config_parser.set('multimedia', 'av_player', config.multimedia.av_player)
        config_parser.set('multimedia', 'av_player_path', config.multimedia.av_player_path)
        config_parser.set('multimedia', 'image_viewer', config.multimedia.image_viewer)
        config_parser.set('multimedia', 'image_viewer_path', config.multimedia.image_viewer_path)

        # Web.
        config_parser.add_section('web')
        config_parser.set('web', 'port', config.web.port)

    ####################################################################################################################
    # Private methods -- Parse.
    ####################################################################################################################

    @staticmethod
    def _contains_space_comma(value):

        for i in range(0, len(value)):
            if value[i].isspace() or value[i] == ',':
                return True

        return False

    @staticmethod
    def _list_from_string(value):

        result = []

        current = ''
        in_quote = False
        for i in range(0, len(value)):
            if in_quote:
                if value[i] == '\'' or value[i] == '"':
                    result.append(current)
                    current = ''
                    in_quote = False
                else:
                    current = current + value[i]
            else:
                if value[i] == '\'' or value[i] == '"':
                    if current == '':
                        in_quote = True
                    else:
                        raise Exception('Invalid configuration: malformed list.')
                elif value[i] == ',':
                    if current != '':
                        result.append(current)
                        current = ''
                else:
                    current = current + value[i]

        if current != '':
            result.append(current)

        return result

    @staticmethod
    def _list_to_string(list_to_convert):

        last_index = len(list_to_convert) - 1
        result = ''

        for i in range(0, last_index):
            if ConfigManager._contains_space_comma(list_to_convert[i]):
                result = result + '\'' + list_to_convert[i] + '\','
            else:
                result = result + list_to_convert[i] + ','

        if ConfigManager._contains_space_comma(list_to_convert[last_index]):
            result = result + '\'' + list_to_convert[last_index] + '\''
        else:
            result = result + list_to_convert[last_index]

        return result
