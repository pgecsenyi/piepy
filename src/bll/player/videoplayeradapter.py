from bll.player.playeradapter import PlayerAdapter

class VideoPlayerAdapter(PlayerAdapter):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, video_dal_retriever, player):
        """
        Calls the base class constructor.

        Parameters
        ----------
        video_dal_retriever : VideoDataHandler
            A reference to the video DAL.
        player : IPlayerHandler
            A reference to the audio and video player.
        """

        ### Call base class constructor.
        super(VideoPlayerAdapter, self).__init__(player)

        ### Attributes from outside.
        self._video_dal_retriever = video_dal_retriever

    ####################################################################################################################
    # Protected overrides.
    ####################################################################################################################

    def _get_file_by_id(self, file_id):

        return self._video_dal_retriever.retrieve_video_path(file_id)

    def _get_subtitle_by_id(self, subtitle_id):

        return self._video_dal_retriever.retrieve_subtitle_path(subtitle_id)
