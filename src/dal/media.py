"""
Media DAL accessor.
"""

from dal.audio.audiodatahandler import AudioDataHandler
from dal.context.dbcontext import DbContext
from dal.image.imagedatahandler import ImageDataHandler
from dal.video.videodatahandler import VideoDataHandler

class MediaDataHandler:
    """
    Media DAL accessor.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(
            self,
            audio_data_handler: AudioDataHandler,
            image_data_handler: ImageDataHandler,
            video_data_handler: VideoDataHandler):

        self._audio_data_handler = audio_data_handler
        self._image_data_handler = image_data_handler
        self._video_data_handler = video_data_handler

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def audio_data_handler(self) -> AudioDataHandler:
        return self._audio_data_handler

    @property
    def image_data_handler(self) -> ImageDataHandler:
        return self._image_data_handler

    @property
    def video_data_handler(self) -> VideoDataHandler:
        return self._video_data_handler

class MediaDataHandlerFactory:

    @staticmethod
    def create(database_path: str) -> MediaDataHandler:

        media_db_context = DbContext(database_path)

        audio_dal = AudioDataHandler(media_db_context)
        image_dal = ImageDataHandler(media_db_context)
        video_dal = VideoDataHandler(media_db_context)

        media_dal = MediaDataHandler(audio_dal, image_dal, video_dal)

        return media_dal
