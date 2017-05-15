from flask import abort
from flask import Blueprint
from flask import jsonify

from dal.configuration.configmanager import ConfigManager

########################################################################################################################
# Routing.
########################################################################################################################

audio_player_adapter = None # pylint: disable=invalid-name

player = Blueprint('player', __name__) # pylint: disable=invalid-name

playlist_manager = None # pylint: disable=invalid-name

video_player_adapter = None # pylint: disable=invalid-name

########################################################################################################################
# Routing.
########################################################################################################################

@player.route('/<string:category>/player/play/<int:item_id>', methods=['GET'])
def route_player_play(category, item_id):
    """
    Plays the item given by ID.

    Parameters
    ----------
    category : str
        The category to which the player to be started belongs.
    item_id : int
        The ID of the item in the selected category.

    Returns
    -------
    A boolean value serialized into a JSON string indicating whether the playing was started successfully.
    """

    # Check category.
    _assert_category(category)

    # Play.
    if category == 'audio':
        return audio_player_adapter.play_from_id(item_id)
    elif category == 'video':
        return video_player_adapter.play_from_id(item_id)

@player.route('/player/<string:operation>', methods=['GET'])
def route_player_simple_operation(operation):
    """
    Performs different operations on player: pause, stop, backward, forward and so on. Does nothing when not playing.

    Parameters
    ----------
    operation : str
        The operation to perform.

    Returns
    -------
    A boolean value serialized into a JSON string indicating whether the operation was successful.
    """

    result = _control_players(operation)

    return jsonify({operation : result})

@player.route('/<string:category>/player/<string:operation>', methods=['GET'])
def route_specific_player_operation(category, operation):
    """
    Performs different operations on player: pause, stop, backward, forward and so on. Does nothing when not playing.

    Parameters
    ----------
    category : str
        The category to which the player to be controlled belongs.
    operation : str
        The operation to perform.

    Returns
    -------
    A boolean value serialized into a JSON string indicating whether the operation was successful.
    """

    # Check category.
    _assert_category(category)

    # Do the requested operation.
    result = _control_players(operation, category)

    return jsonify({operation : result})

########################################################################################################################
# Private functions.
########################################################################################################################

def _assert_category(category):
    """
    Checks if the selected category exists in the list of categories. If not, aborts.

    Parameters
    ----------
    category : str
        The category to check.
    """

    if category not in ConfigManager.categories:
        abort(404)

def _control_players(operation, category=None):

    are_all_players_active = (category is None) or (category.strip() == '')
    player_adapters = _get_player_adapters_for_category(category)
    result = False

    if are_all_players_active and operation == 'stop':
        result = playlist_manager.stop()

    result = _execute_operation_on_players(player_adapters, operation) or result

    return result

def _execute_operation_on_players(player_adapters, operation):

    result = False

    for player_adapter in player_adapters:
        if operation == 'faster':
            result = player_adapter.player.faster() or result
        elif operation == 'fastforward':
            result = player_adapter.player.fast_forward() or result
        elif operation == 'fastrewind':
            result = player_adapter.player.fast_rewind() or result
        elif operation == 'forward':
            result = player_adapter.player.forward() or result
        elif operation == 'pause':
            result = player_adapter.player.pause() or result
        elif operation == 'rewind':
            result = player_adapter.player.rewind() or result
        elif operation == 'slower':
            result = player_adapter.player.slower() or result
        elif operation == 'stop':
            result = player_adapter.player.stop() or result
        elif operation == 'volumedown':
            result = player_adapter.player.volume_down() or result
        elif operation == 'volumeup':
            result = player_adapter.player.volume_up() or result
        else:
            abort(404)

    return result

def _get_player_adapters_for_category(category):

    is_category_provided = (category != None) and (category.strip() != '')
    player_adapters = []

    if (not is_category_provided) or (category == 'audio'):
        player_adapters.append(audio_player_adapter)
    if (not is_category_provided) or (category == 'video'):
        player_adapters.append(video_player_adapter)

    return player_adapters
