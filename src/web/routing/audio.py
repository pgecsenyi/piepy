from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request

########################################################################################################################
# Initialization.
########################################################################################################################

audio = Blueprint('audio', __name__) # pylint: disable=invalid-name

audio_dal_retriever = None # pylint: disable=invalid-name

audio_player_adapter = None # pylint: disable=invalid-name

########################################################################################################################
# Routing.
########################################################################################################################

@audio.route('/audio/albums')
def route_audio_albums():
    """
    Lists the albums.
    """

    artist_id = None
    if (request.args is not None) and ('artist' in request.args):
        artist_id = request.args['artist']

    result = audio_dal_retriever.retrieve_albums(artist_id)
    return jsonify({'albums' : result})

@audio.route('/audio/artists')
def route_audio_artists():
    """
    Lists details for the given title.
    """

    result = audio_dal_retriever.retrieve_artists()
    return jsonify({'artists' : result})

@audio.route('/audio/player/play', methods=['GET'])
def route_audio_player_play():
    """
    Plays the audio file given by ID.
    """

    return audio_player_adapter.play_from_arguments(request.args)

@audio.route('/audio/tracks')
def route_audio_tracks():
    """
    Lists all available tracks.
    """

    if request.args is None or 'album' not in request.args:
        abort(400)

    album_id = request.args['album']
    result = audio_dal_retriever.retrieve_tracks(album_id)

    return jsonify({'tracks' : result})
