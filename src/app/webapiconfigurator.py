"""
Implements web interface configurator logic.
"""

import datetime

from bll.mediacatalog.catalogizer import Catalogizer
from bll.mediacatalog.catalogizercontext import CatalogizerContext
from bll.player.audioplayeradapter import AudioPlayerAdapter
from bll.player.videoplayeradapter import VideoPlayerAdapter
from bll.playlist.playlistmanager import PlaylistManager
from dal.configuration.config import IndexingConfig
from dal.configuration.configmanager import ConfigManager
from dal.context.dbcontext import DbContext
from dal.media import MediaDataHandler
from multimedia.imageviewerhandler import ImageViewerHandler
from multimedia.imageviewerhandlers.fbiimageviewerhandler import FbiImageViewerHandler
from multimedia.imageviewerhandlers.fehimageviewerhandler import FehImageViewerHandler
from multimedia.playerhandler import PlayerHandler
from multimedia.playlist.playlisthandler import PlaylistHandler
import web.routing.audio
import web.routing.image
import web.routing.maintenance
import web.routing.player
import web.routing.playlist
import web.routing.video
from web.statusinfo import StatusInfo

class WebApiConfigurator(object):
    """
    Implements web interface configurator logic.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(
            self,
            media_dal: MediaDataHandler,
            audio_player: PlayerHandler,
            video_player: PlayerHandler,
            playlist_handler: PlaylistHandler):

        self._media_dal = media_dal
        self._audio_player = audio_player
        self._video_player = video_player
        self._playlist_handler = playlist_handler

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def configure_interfaces(self):

        self._configure_audio()
        self._configure_image()
        self._configure_video()
        self._configure_maintenance()
        self._configure_player()
        self._configure_playlist()

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _configure_audio(self):

        audio_dal = self._media_dal.audio_data_handler
        web.routing.audio.audio_dal_retriever = audio_dal.retriever
        web.routing.audio.audio_player_adapter = AudioPlayerAdapter(audio_dal.retriever, self._audio_player)

    def _configure_video(self):

        video_dal = self._media_dal.video_data_handler
        web.routing.video.video_dal_retriever = video_dal.retriever
        web.routing.video.video_player_adapter = VideoPlayerAdapter(video_dal.retriever, self._video_player)

    def _configure_image(self):

        image_dal = self._media_dal.image_data_handler
        image_viewer = self._create_image_viewer()

        web.routing.image.image_dal = image_dal
        web.routing.image.image_viewer = image_viewer

    def _create_image_viewer(self) -> ImageViewerHandler:
        """
        Creates an Image Viewer Handler.

        Returns
        -------
        The new ImageViewerHandler instance.
        """

        image_viewer = None

        if ConfigManager.settings.multimedia.image_viewer == 'fbi':
            image_viewer = FbiImageViewerHandler(ConfigManager.settings.multimedia.image_viewer_path)
        elif ConfigManager.settings.multimedia.image_viewer == 'feh':
            image_viewer = FehImageViewerHandler(ConfigManager.settings.multimedia.image_viewer_path)
        else:
            raise Exception('Invalid image viewer.')

        return image_viewer

    def _configure_maintenance(self):

        catalogizer_context = self._create_catalogizer_context()

        web.routing.maintenance.catalogizer = Catalogizer(catalogizer_context)
        web.routing.maintenance.status_info = StatusInfo(
            datetime.datetime.now(),
            self._media_dal.audio_data_handler,
            self._media_dal.image_data_handler,
            self._media_dal.video_data_handler)
        web.routing.maintenance.video_dal_retriever = self._media_dal.video_data_handler.retriever

    def _create_catalogizer_context(self) -> CatalogizerContext:

        catalogizer_context = CatalogizerContext()
        catalogizer_context.database_config = ConfigManager.settings.database
        catalogizer_context.indexing_config = self._create_indexer_configuration()
        catalogizer_context.media_dal = self._media_dal

        return catalogizer_context

    def _create_indexer_configuration(self) -> IndexingConfig:
        """
        Creates runtime Indexer configuration based on persisted settings.

        Returns
        -------
        The new IndexingConfig instance.
        """

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

    def _configure_player(self):

        web.routing.player.audio_player_adapter = web.routing.audio.audio_player_adapter
        web.routing.player.playlist_handler = self._playlist_handler
        web.routing.player.video_player_adapter = web.routing.video.video_player_adapter

    def _configure_playlist(self):

        playlist_db_context = DbContext(ConfigManager.settings.database.path_playlist)

        playlist_manager = PlaylistManager(playlist_db_context, self._playlist_handler)
        playlist_manager.audio_retriever = self._media_dal.audio_data_handler.retriever
        playlist_manager.video_retriever = self._media_dal.video_data_handler.retriever

        web.routing.playlist.playlist_manager = playlist_manager
