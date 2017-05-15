from bll.player.playeradapter import PlayerAdapter

class AudioPlayerAdapter(PlayerAdapter):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, audio_dal_retriever, player):
        """
        Calls the base class constructor.

        Parameters
        ----------
        audio_dal_retriever : AudioDataHandler
            A reference to the audio DAL.
        player : IPlayerHandler
            A reference to the audio and video player.
        """

        ### Call base class constructor.
        super(AudioPlayerAdapter, self).__init__(player)

        ### Attributes from outside.
        self._audio_dal_retriever = audio_dal_retriever

    ####################################################################################################################
    # Protected overrides.
    ####################################################################################################################

    def _get_file_by_id(self, file_id):

        return self._audio_dal_retriever.retrieve_path(file_id)

    def _get_subtitle_by_id(self, file_id):

        return None
