import datetime

class StatusInfo(object):

    ####################################################################################################################
    # Static attributes.
    ####################################################################################################################

    CACHE_UPDATE_INTERVAL = 1800

    AUDIO_COUNT = 'audio_count'
    IMAGE_COUNT = 'image_count'
    LAST_SYNC_DURATION = 'last_sync_duration'
    LAST_SYNC_TIME = 'last_sync_time'
    STARTUP_TIME = 'startup_time'
    VIDEO_COUNT = 'video_count'

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, startup_time, audio_dal, image_dal, video_dal):

        ### Attributes from outside.
        self._audio_dal = audio_dal
        self._image_dal = image_dal
        self._video_dal = video_dal

        ### Private attributes.
        self._last_update = None
        self._status = {
            StatusInfo.AUDIO_COUNT: 0,
            StatusInfo.IMAGE_COUNT: 0,
            StatusInfo.LAST_SYNC_DURATION: None,
            StatusInfo.LAST_SYNC_TIME: None,
            StatusInfo.STARTUP_TIME: startup_time,
            StatusInfo.VIDEO_COUNT: 0}

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def audio_count(self):
        """
        Gets the number of audio files.
        """
        return self._status[StatusInfo.AUDIO_COUNT]

    @property
    def image_count(self):
        """
        Gets the number of image files.
        """
        return self._status[StatusInfo.IMAGE_COUNT]

    @property
    def last_sync_duration(self):
        """
        Gets the duration of the last synchronization.
        """
        return self._status[StatusInfo.LAST_SYNC_DURATION]

    @last_sync_duration.setter
    def last_sync_duration(self, value):
        """
        Sets the duration of the last synchronization.
        """
        self._status[StatusInfo.LAST_SYNC_DURATION] = value

    @property
    def last_sync_time(self):
        """
        Gets the time of the last synchronization.
        """
        return self._status[StatusInfo.LAST_SYNC_TIME]

    @last_sync_time.setter
    def last_sync_time(self, value):
        """
        Sets the time of the last synchronization.
        """
        self._status[StatusInfo.LAST_SYNC_TIME] = value

    @property
    def uptime(self):
        """
        Gets the uptime.
        """
        return datetime.datetime.now() - self._status[StatusInfo.STARTUP_TIME]

    @property
    def video_count(self):
        """
        Gets the number of image files.
        """
        return self._status[StatusInfo.VIDEO_COUNT]

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def refresh(self):

        if self._last_update is None:
            self._update_cache()
        else:
            now = datetime.datetime.now()
            diff = (now - self._last_update).total_seconds()
            if diff > StatusInfo.CACHE_UPDATE_INTERVAL:
                self._update_cache()

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _update_cache(self):

        self._status[StatusInfo.AUDIO_COUNT] = self._audio_dal.retriever.retrieve_file_count()
        self._status[StatusInfo.IMAGE_COUNT] = self._image_dal.retriever.retrieve_file_count()
        self._status[StatusInfo.VIDEO_COUNT] = self._video_dal.retriever.retrieve_file_count()

        self._last_update = datetime.datetime.now()
