"""
Main module.

Initializes and configures server, publishes the REST API.
"""

import configparser

from flask import Flask

from app.argumentparser import ArgumentParser
from app.loggingconfigurator import LoggingConfigurator
from app.webapiconfigurator import WebApiConfigurator
from bll.userdatamanager import UserDataManager
from dal.configuration.configmanager import ConfigManager
from dal.media import MediaDataHandler, MediaDataHandlerFactory
from multimedia.playerhandler import PlayerHandler
from multimedia.playerhandlers.omxplayerhandler import OmxPlayerHandler
from multimedia.playerhandlers.vlcplayerhandler import VlcPlayerHandler
from multimedia.playlist.playlisthandler import PlaylistHandler
import web.routing.audio
import web.routing.image
import web.routing.maintenance
import web.routing.player
import web.routing.playlist
import web.routing.video

def initialize():
    """
    Parses command line arguments and initializes the application: internal modules as well as Flask.
    """

    # Parse command line arguments.
    argument_parser = ArgumentParser()
    argument_parser.parse_arguments()

    # Load configuration.
    load_configuration(argument_parser.config_file_path)

    # Initialize internal modules.
    initialize_internal_modules()

    # Initialize flask.
    app = Flask(__name__)
    initialize_flask(app)

    # Configure logging.
    logging_configurator = LoggingConfigurator(argument_parser.is_debugging_enabled, argument_parser.log_file_path)
    logging_configurator.configure_logging()

    # Go.
    app.run(host='0.0.0.0', port=ConfigManager.settings.web.port, debug=argument_parser.is_debugging_enabled)

def load_configuration(config_file_path: str):
    """
    Loads configuration from the given file.

    Parameters
    ----------
    config_file_path : str
        The path of the configuration file.
    """

    try:
        ConfigManager.load(config_file_path)
    except configparser.NoOptionError as exception:
        print('Invalid configuration file, missing option... ' + exception.args[0])
        exit(1)
    except configparser.NoSectionError as exception:
        print('Invalid configuration file, missing section... ' + exception.args[0])
        exit(1)
    except Exception as exception:
        print(exception.args[0])
        exit(1)

def initialize_internal_modules():
    """
    Initializes internal modules: Data Access Layer, Image Viewer, Player Handler and the Indexer.
    """

    media_dal = MediaDataHandlerFactory.create(ConfigManager.settings.database.path_media)
    initialize_web_api(media_dal)
    initialize_user_data_manager()

def initialize_web_api(media_dal: MediaDataHandler):
    """
    Initializes web API.
    """

    audio_player = create_player()
    video_player = create_player()
    playlist_handler = create_playlist_handler(audio_player, video_player)

    wic = WebApiConfigurator(media_dal, audio_player, video_player, playlist_handler)
    wic.configure_interfaces()

def create_player() -> PlayerHandler:
    """
    Creates a Multimedia Player Handler.

    Returns
    -------
    The new PlayerHandler instance.
    """

    player = None

    if ConfigManager.settings.multimedia.av_player == 'omxplayer':
        player = OmxPlayerHandler(ConfigManager.settings.multimedia.av_player_path)
    elif ConfigManager.settings.multimedia.av_player == 'vlc':
        player = VlcPlayerHandler(ConfigManager.settings.multimedia.av_player_path)
    else:
        raise Exception('Invalid player.')

    return player

def create_playlist_handler(audio_player: PlayerHandler, video_player: PlayerHandler) -> PlaylistHandler:
    """
    Creates a Playlist Handler.

    Parameters
    ----------
    audio_player : PlayerHandler
        The Audio Player Handler.
    video_player : PlayerHandler
        The Video Player Handler.

    Returns
    -------
    The new PlaylistHandler instance.
    """

    default_playlist_player = create_player()

    playlist_handler = PlaylistHandler(default_playlist_player)
    playlist_handler.set_player_handler('audio', audio_player)
    playlist_handler.set_player_handler('video', video_player)

    return playlist_handler

def initialize_user_data_manager():
    """
    Initializes User Data Manager.
    """

    user_data_manager = UserDataManager()
    user_data_manager.create_playlist_storage(
        web.routing.playlist.playlist_manager,
        ConfigManager.settings.database.path_playlist)

def initialize_flask(app: str):
    """
    Initializes Flask, registers Blueprints.

    Parameters
    ----------
    app : str
        The name of the Flask instance.
    """

    app.register_blueprint(web.routing.audio.audio)
    app.register_blueprint(web.routing.maintenance.maintenance)
    app.register_blueprint(web.routing.image.image)
    app.register_blueprint(web.routing.player.player)
    app.register_blueprint(web.routing.playlist.playlist)
    app.register_blueprint(web.routing.video.video)
