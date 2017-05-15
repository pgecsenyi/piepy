from os import path

from flask import abort
from flask import jsonify

from multimedia.constants import AUDIO_OUTPUT_ANALOG, AUDIO_OUTPUT_DIGITAL

class PlayerAdapter(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, player):

        ### Attributes from outside.
        self._player = player

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def player(self):
        """
        Gets the internal player handler.
        """
        return self._player

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def play_from_arguments(self, arguments):

        # File id is given as a request argument.
        if (arguments is None) or (len(arguments) <= 0) or ('id' not in arguments):
            abort(404)

        # Check category, get filename from database.
        file_to_play = self._get_file_by_id(arguments['id'])

        # Check if the result makes sense and the given file exists.
        if (file_to_play is None) or (file_to_play.strip() == '') or not path.exists(file_to_play):
            abort(404)

        # Choose audio output.
        audio_output = AUDIO_OUTPUT_DIGITAL
        if 'audioout' in arguments:
            if arguments['audioout'] == 'analog':
                audio_output = AUDIO_OUTPUT_ANALOG

        # Get subtitle path from database.
        subtitle_to_use = None
        if 'subtitle' in arguments:
            subtitle_to_use = self._get_subtitle_by_id(arguments['subtitle'])

        # Check if the given subtitle file exists.
        if subtitle_to_use != None and not path.exists(subtitle_to_use):
            return None

        # Play.
        result = self._player.play(audio_output, file_to_play, subtitle_to_use)

        return jsonify({'play' : result})

    def play_from_id(self, item_id):

        # File id is given as a request argument.
        if item_id is None:
            abort(404)

        # Get path from database.
        file_to_play = self._get_file_by_id(item_id)

        # Check if the result makes sense.
        if (file_to_play is None) or (file_to_play == ''):
            abort(404)

        # Play.
        result = self._player.play(AUDIO_OUTPUT_DIGITAL, file_to_play)

        return jsonify({'play' : result})

    ####################################################################################################################
    # Protected overrideables.
    ####################################################################################################################

    def _get_file_by_id(self, file_id):
        pass

    def _get_subtitle_by_id(self, file_id):
        pass
