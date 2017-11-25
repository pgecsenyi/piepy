"""
PiEPy server main

Initializes server, publishes REST API and does the routing.
"""

import configparser
import datetime
import getopt
import logging
import logging.handlers
import sys
from flask import Flask

from bll.mediacatalog.catalogizer import Catalogizer
from bll.mediacatalog.catalogizercontext import CatalogizerContext
from bll.player.audioplayeradapter import AudioPlayerAdapter
from bll.player.videoplayeradapter import VideoPlayerAdapter
from bll.playlist.playlistmanager import PlaylistManager
from bll.userdatamanager import UserDataManager
from dal.audio.audiodatahandler import AudioDataHandler
from dal.configuration.config import Config, IndexingConfig
from dal.configuration.configmanager import ConfigManager
from dal.context.dbcontext import DbContext
from dal.image.imagedatahandler import ImageDataHandler
from dal.video.videodatahandler import VideoDataHandler
from multimedia.imageviewerhandlers.fbiimageviewerhandler import FbiImageViewerHandler
from multimedia.imageviewerhandlers.fehimageviewerhandler import FehImageViewerHandler
from multimedia.playerhandlers.omxplayerhandler import OmxPlayerHandler
from multimedia.playerhandlers.vlcplayerhandler import VlcPlayerHandler
import multimedia.playlist.playlisthandler
import web.routing.audio
import web.routing.image
import web.routing.maintenance
import web.routing.player
import web.routing.playlist
import web.routing.video
from web.statusinfo import StatusInfo

########################################################################################################################
# Parameters.
########################################################################################################################

_default_config_file_path = 'config.cfg' # pylint: disable=invalid-name

########################################################################################################################
# Functions.
########################################################################################################################

def configure_logging(is_debugging_enabled=False, log_path_override=None):
    """
    Configures logging based on the provided parameters: enables or disables logging into a file or to the console and
    sets the debug level as well. Makes use of Python's built-in logging module.

    Parameters
    ----------
    is_debugging_enabled : boolean
        Indicates whether the application is running in debug mode.
    log_path_override : str
        The path of the log file to use. If set to None, then the application will use the path provided in the
        configuration file.
    """

    logger = logging.getLogger()

    logging_config = ConfigManager.settings.logging
    log_level = determine_log_level(is_debugging_enabled)
    log_path = determine_log_path(log_path_override)
    is_logging_possible = logging_config.enabled and (log_path is not None) and (logging_config.max_size_bytes > 0)

    logger.setLevel(log_level)

    # If debugging is enabled, log to the command line on DEBUG level by all means.
    if is_debugging_enabled:
        logger.addHandler(logging.StreamHandler())
    elif not is_logging_possible:
        logger.addHandler(logging.NullHandler())
        logger.propagate = False

    # If path is set, log to file.
    if is_logging_possible:
        logger.addHandler(logging.handlers.RotatingFileHandler(
            filename=log_path,
            maxBytes=logging_config.max_size_bytes,
            backupCount=3))

def configure_routing_audio_video(audio_dal, video_dal, audio_player, video_player):

    web.routing.audio.audio_dal_retriever = audio_dal.retriever
    web.routing.audio.audio_player_adapter = AudioPlayerAdapter(audio_dal.retriever, audio_player)

    web.routing.video.video_dal_retriever = video_dal.retriever
    web.routing.video.video_player_adapter = VideoPlayerAdapter(video_dal.retriever, video_player)

def configure_routing_image(image_dal):

    image_viewer = create_image_viewer()

    web.routing.image.image_dal = image_dal
    web.routing.image.image_viewer = image_viewer

def configure_routing_maintenance(audio_dal, image_dal, video_dal):

    catalogizer_context = CatalogizerContext()
    catalogizer_context.database_config = ConfigManager.settings.database
    catalogizer_context.indexing_config = create_indexer_configuration()
    catalogizer_context.audio_dal = audio_dal
    catalogizer_context.image_dal = image_dal
    catalogizer_context.video_dal = video_dal

    web.routing.maintenance.catalogizer = Catalogizer(catalogizer_context)
    web.routing.maintenance.status_info = StatusInfo(datetime.datetime.now(), audio_dal, image_dal, video_dal)
    web.routing.maintenance.video_dal_retriever = video_dal.retriever

def configure_routing_player(playlist_handler):

    web.routing.player.audio_player_adapter = web.routing.audio.audio_player_adapter
    web.routing.player.playlist_handler = playlist_handler
    web.routing.player.video_player_adapter = web.routing.video.video_player_adapter

def configure_routing_playlist(audio_dal, video_dal, playlist_handler):

    playlist_db_context = DbContext(ConfigManager.settings.database.path_playlist)

    playlist_manager = PlaylistManager(playlist_db_context, playlist_handler)
    playlist_manager.audio_retriever = audio_dal.retriever
    playlist_manager.video_retriever = video_dal.retriever

    web.routing.playlist.playlist_manager = playlist_manager

def create_image_viewer():

    image_viewer = None

    if ConfigManager.settings.multimedia.image_viewer == 'fbi':
        image_viewer = FbiImageViewerHandler(ConfigManager.settings.multimedia.image_viewer_path)
    elif ConfigManager.settings.multimedia.image_viewer == 'feh':
        image_viewer = FehImageViewerHandler(ConfigManager.settings.multimedia.image_viewer_path)
    else:
        raise Exception('Invalid image viewer.')

    return image_viewer

def create_indexer_configuration():

    indexing_config = IndexingConfig()

    indexing_config.audio = None
    if 'audio' in ConfigManager.categories:
        indexing_config.audio = ConfigManager.settings.indexing.audio
    indexing_config.image = None
    if 'image' in ConfigManager.categories:
        indexing_config.image = ConfigManager.settings.indexing.image
    indexing_config.video = None
    if 'video' in ConfigManager.categories:
        indexing_config.video = ConfigManager.settings.indexing.video

    return indexing_config

def create_player():

    player = None

    if ConfigManager.settings.multimedia.av_player == 'omxplayer':
        player = OmxPlayerHandler(ConfigManager.settings.multimedia.av_player_path)
    elif ConfigManager.settings.multimedia.av_player == 'vlc':
        player = VlcPlayerHandler(ConfigManager.settings.multimedia.av_player_path)
    else:
        raise Exception('Invalid player.')

    return player

def create_playlist_handler(audio_player, video_player):

    default_playlist_player = create_player()

    playlist_handler = multimedia.playlist.playlisthandler.PlaylistHandler(default_playlist_player)
    playlist_handler.set_player_handler('audio', audio_player)
    playlist_handler.set_player_handler('video', video_player)

    return playlist_handler

def determine_log_level(is_debugging_enabled):

    if is_debugging_enabled:
        return logging.DEBUG

    logging_config = ConfigManager.settings.logging

    if logging_config.level is not None:
        if logging_config.level == 'critical':
            return logging.CRITICAL
        elif logging_config.level == 'debug':
            return logging.DEBUG
        elif logging_config.level == 'info':
            return logging.INFO
        elif logging_config.level == 'warning':
            return logging.WARNING

    return logging.ERROR

def determine_log_path(log_path_override=None):

    logging_config = ConfigManager.settings.logging

    if log_path_override is not None:
        return log_path_override
    elif logging_config.path is not None:
        return logging_config.path

    return None

def generate_config_and_exit(config_file_path):
    """
    Generates a default configuration file and exists the application.

    Parameters
    ----------
    config_file_path : str
        The path where the generated file has to be saved.
    """

    config = Config()
    config.create_default()
    ConfigManager.save(config_file_path, config)

    print('Configuration file successfully generated to {0}.'.format(config_file_path))
    sys.exit(0)

def initialize(config_file_path, application_name, arguments):
    """
    Parses command line arguments and initializes the application: internal modules as well as Flask.

    Parameters
    ----------
    config_file_path : str
        The path of the configuration file.
    application_name : str
        The name of the application (used in console messages).
    arguments : list of str
        The list of the command line arguments, excluding application name.
    """

    # Parse command line arguments.
    is_config_generation_requested = False
    is_debugging_enabled = False
    log_file_path = None

    try:
        opts, _ = getopt.getopt(arguments, 'c:dhil:', ['config=', 'debug', 'help', 'install', 'log'])
    except getopt.GetoptError:
        print_usage_and_exit(application_name, 2)

    for opt, arg in opts:
        if opt in ('-c', '--config'):
            config_file_path = arg
        elif opt in ('-d', '--debug'):
            is_debugging_enabled = True
        elif opt in ('-h', '--help'):
            print_usage_and_exit(application_name)
        elif opt in ('-i', '--install'):
            is_config_generation_requested = True
        elif opt in ('-l', '--log'):
            log_file_path = arg

    # Generate config if requested.
    if is_config_generation_requested:
        generate_config_and_exit(config_file_path)

    # Load configuration.
    load_configuration(config_file_path)

    # Initialize internal modules.
    initialize_internal_modules()

    # Initialize flask and configure logging.
    app = Flask(__name__)
    initialize_flask(app)
    configure_logging(is_debugging_enabled, log_file_path)

    # Go.
    app.run(host='0.0.0.0', port=ConfigManager.settings.web.port, debug=is_debugging_enabled)

def initialize_flask(app):
    """
    Initializes Flask, registers Blueprints.

    Parameters
    ----------
    app : object
        The Flask instance.
    """

    app.register_blueprint(web.routing.audio.audio)
    app.register_blueprint(web.routing.maintenance.maintenance)
    app.register_blueprint(web.routing.image.image)
    app.register_blueprint(web.routing.player.player)
    app.register_blueprint(web.routing.playlist.playlist)
    app.register_blueprint(web.routing.video.video)

def initialize_internal_modules():
    """
    Initializes internal modules: Data Access Layer, Image Viewer, Player Handler and the Indexer.
    """

    media_db_context = DbContext(ConfigManager.settings.database.path_media)

    audio_dal = AudioDataHandler(media_db_context)
    image_dal = ImageDataHandler(media_db_context)
    video_dal = VideoDataHandler(media_db_context)

    audio_player = create_player()
    video_player = create_player()
    playlist_handler = create_playlist_handler(audio_player, video_player)

    configure_routing_audio_video(audio_dal, video_dal, audio_player, video_player)
    configure_routing_image(image_dal)
    configure_routing_maintenance(audio_dal, image_dal, video_dal)
    configure_routing_player(playlist_handler)
    configure_routing_playlist(audio_dal, video_dal, playlist_handler)

    user_data_manager = UserDataManager()
    user_data_manager.create_playlist_storage(
        web.routing.playlist.playlist_manager,
        ConfigManager.settings.database.path_playlist)

def load_configuration(config_file_path):
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

def main(argv):
    """
    The entry point.

    Parameters
    ----------
    argv : list of str
        The list of command line arguments.
    """

    initialize(_default_config_file_path, argv[0], argv[1:])

def print_usage_and_exit(application_name, error_code=0):
    """
    Prints a short manual and exists the application.

    Parameters
    ----------
    application_name : str
        The name of the application (used in console messages).
    error_code : int
        The error code to exit with.
    """

    print('python {0} <options>'.format(application_name))
    print('')
    print('  -c, --config    Use the specified configuration file instead')
    print('                  of the default ({0}) one.'.format(_default_config_file_path))
    print('  -d, --debug     Run the application in debug mode.')
    print('  -h, --help      Print this help and exit.')
    print('  -i, --install   Generate a sample configuration file and exit.')
    print('  -l, --log       Log to the specified file.')
    print('')
    print(
        'Run the application as a member of the \'video\' group. In case you would like to use port 80, run the '
        'application as superuser.')
    sys.exit(error_code)
