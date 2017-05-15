from multimedia.constants import AUDIO_OUTPUT_DIGITAL

class PlayingState(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, track_id, player_handler):

        self._track_id = track_id
        self._player_handler = player_handler

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def player_handler(self):
        return self._player_handler

    @player_handler.setter
    def player_handler(self, value):
        self._player_handler = value

    @property
    def track_id(self):
        return self._track_id

    @track_id.setter
    def track_id(self, value):
        self._track_id = value

class PlaylistTrack(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, track_id, path, label):

        ### Validate parameters.
        if path is None:
            raise Exception('path cannot be None.')

        ### Attributes from outside.
        # The ID of this item.
        self.track_id = track_id
        # The path of this item.
        self.path = path
        # The label for this item (which can be used for e.g. identifying the player to be used).
        self.label = label

        ### Private attributes.
        # Stores the chosen audio output for this item.
        self._audio_output = AUDIO_OUTPUT_DIGITAL
        # Stores the chosen subtitle for this item.
        self._subtitle_path = None

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def audio_output(self):
        """
        Gets the chosen audio output for this item.
        """
        return self._audio_output

    @audio_output.setter
    def audio_output(self, value):
        """
        Sets the audio output for this node.
        """
        self._audio_output = value

    @property
    def subtitle_path(self):
        """
        Gets the subtitle for this item.
        """
        return self._subtitle_path

    @subtitle_path.setter
    def subtitle_path(self, value):
        """
        Sets the subtitle for this item.
        """
        self._subtitle_path = value
