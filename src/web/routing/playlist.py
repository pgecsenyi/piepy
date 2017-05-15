from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

from bll.playlist.entities import NewPlaylist
from bll.playlist.entities import NewPlaylistTrack
from dal.configuration.configmanager import ConfigManager
from web.util.functions import to_audio_output_multimedia, to_audio_output_string

########################################################################################################################
# Initialization.
########################################################################################################################

playlist = Blueprint('playlist', __name__) # pylint: disable=invalid-name

playlist_manager = None # pylint: disable=invalid-name

########################################################################################################################
# Routing.
########################################################################################################################

@playlist.route('/playlist/add', methods=['PUT'])
def route_playlist_add_playlist():
    """
    Creates a new playlist.

    Returns
    -------
    A JSON string containing the playlist header.
    """

    # Validate request.
    _validate_request_arguments(['title', 'tracks'])

    # Do the necessary conversion.
    title = request.json['title']
    tracks = _new_tracks_to_bll(request.json['tracks'])
    new_playlist_bll = NewPlaylist(title, tracks)

    # Save the new playlist to the database and send back the result.
    playlist_header_bll = playlist_manager.add_playlist(new_playlist_bll)
    playlist_header_json = _playlist_header_to_json(playlist_header_bll)

    return jsonify({'playlist' : playlist_header_json})

@playlist.route('/playlist/add-track', methods=['PUT'])
def route_playlist_add_track():
    """
    Adds the given track to the given playlist.

    Returns
    -------
    The saved track serialized into a JSON string.
    """

    # Validate request.
    _validate_request_arguments(['playlist', 'category', 'file'])
    _validate_category(request.json['category'])

    # Do the necessary conversions.
    number_after = 0
    if number_after in request.json:
        number_after = request.json['number_after']
    new_track_bll = _new_track_to_bll(request.json)

    # Save the new track to the database and send back the result.
    track_bll = playlist_manager.add_track(request.json['playlist'], new_track_bll, number_after)
    track_json = _track_to_json(track_bll)

    return jsonify({'track' : track_json})

@playlist.route('/playlist/delete/<int:playlist_id>', methods=['DELETE'])
def route_playlist_delete_playlist(playlist_id):
    """
    Deletes the given playlist.

    Returns
    -------
    True.
    """

    playlist_manager.delete_playlist(playlist_id)

    return jsonify({'delete' : True})

@playlist.route('/playlist/delete-track/<int:track_id>', methods=['DELETE'])
def route_playlist_delete_track(track_id):
    """
    Removes the specified item from it's playlist.

    Returns
    -------
    A boolean value serialized into a JSON string indicating whether the item was found and removed from the list.
    """

    playlist_manager.delete_track(track_id)

    return jsonify({'delete' : True})

@playlist.route('/playlist/play/<int:playlist_id>', methods=['GET'])
def route_playlist_play(playlist_id):
    """
    Starts playing the playlist.

    Returns
    -------
    A boolean value serialized into a JSON string indicating whether the first item on the playlist is valid and player
    was started successfully.
    """

    result = playlist_manager.play(playlist_id)

    return jsonify({'play' : result})

@playlist.route('/playlist/next', methods=['GET'])
def route_playlist_play_next():
    """
    Plays the next track.
    """

    playlist_manager.next()

    return ''

@playlist.route('/playlist/prev', methods=['GET'])
def route_playlist_play_previous():
    """
    Plays the previous track.
    """

    playlist_manager.previous()

    return ''

@playlist.route('/playlist/stop', methods=['GET'])
def route_playlist_play_stop():
    """
    Stops the playing of the playlist.

    Returns
    -------
    A boolean value serialized into a JSON string indicating whether the playing was stopped succesfully.
    """

    result = playlist_manager.stop()

    return jsonify({'stop' : result})

@playlist.route('/playlist/all', methods=['GET'])
def route_playlist_view_all():
    """
    Retrieves all playlists.

    Returns
    -------
    The list of the playlists serialized into a JSON string.
    """

    result = _playlist_headers_to_json(playlist_manager.retrieve_playlist_headers())

    return jsonify({'playlists' : result})

@playlist.route('/playlist/current', methods=['GET'])
def route_playlist_view_current():
    """
    Retrieves all playlists.

    Returns
    -------
    The list of the playlists serialized into a JSON string.
    """

    result = _playlist_to_json(playlist_manager.retrieve_playlist())

    return jsonify({'playlist' : result})

@playlist.route('/playlist/<int:playlist_id>', methods=['GET'])
def route_playlist_view_by_id(playlist_id):
    """
    Retrieves the details of a given playlist.

    Returns
    -------
    The list of the playlists serialized into a JSON string.
    """

    result = _playlist_to_json(playlist_manager.retrieve_playlist(playlist_id))

    return jsonify({'playlist' : result})

########################################################################################################################
# Private methods -- validation.
########################################################################################################################

def _validate_category(category):
    """
    Checks if the selected category exists in the list of categories. If not, aborts.

    Parameters
    ----------
    category : str
        The category to check.
    """

    if category not in ConfigManager.categories:
        abort(404)

def _validate_request_arguments(required_arguments):

    if (request.json is None) or (len(request.json) <= 0):
        abort(400)

    for required_argument in required_arguments:
        if required_argument not in request.json:
            abort(400)

########################################################################################################################
# Private methods -- conversion.
########################################################################################################################

def _new_track_to_bll(new_track_json):

    if new_track_json is None:
        return None

    new_track_bll = NewPlaylistTrack(new_track_json['category'], new_track_json['file'])
    new_track_bll.audio_output = to_audio_output_multimedia(new_track_json)

    return new_track_bll

def _new_tracks_to_bll(new_tracks_json):

    if new_tracks_json is None:
        return None

    new_tracks_bll = []
    for new_track_json in new_tracks_json:
        new_tracks_bll.append(_new_track_to_bll(new_track_json))

    return new_tracks_bll

def _playlist_header_to_json(playlist_header_bll):

    if playlist_header_bll is None:
        return None

    playlist_header_json = {
        'id' : playlist_header_bll.playlist_id,
        'title' : playlist_header_bll.title}

    return playlist_header_json

def _playlist_headers_to_json(playlist_headers_bll):

    if playlist_headers_bll is None:
        return None

    playlist_headers_json = []
    for playlist_header_bll in playlist_headers_bll:
        playlist_headers_json.append(_playlist_header_to_json(playlist_header_bll))

    return playlist_headers_json

def _playlist_to_json(playlist_bll):

    if playlist_bll is None:
        return None

    playlist_json = {
        'id' : playlist_bll.playlist_id,
        'title' : playlist_bll.title,
        'tracks' : _tracks_to_json(playlist_bll.tracks)}

    return playlist_json

def _track_to_json(track_bll, number=0):

    if track_bll is None:
        return None

    track_json = {
        'id' : track_bll.track_id,
        'category' : track_bll.category,
        'title' : track_bll.title,
        'audioout' : to_audio_output_string(track_bll.audio_output),
    }

    if number > 0:
        track_json['number'] = number

    return track_json

def _tracks_to_json(tracks_bll):

    tracks_json = []
    for i in range(0, len(tracks_bll)):
        number = i + 1
        tracks_json.append(_track_to_json(tracks_bll[i], number))

    return tracks_json
