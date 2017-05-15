from flask import Blueprint
from flask import jsonify
from flask import request

from dal.video.videotitlefilter import VideoTitleFilter

########################################################################################################################
# Initialization.
########################################################################################################################

video = Blueprint('video', __name__) # pylint: disable=invalid-name

video_dal_retriever = None # pylint: disable=invalid-name

video_player_adapter = None # pylint: disable=invalid-name

########################################################################################################################
# Routing.
########################################################################################################################

@video.route('/video/details/<int:id_title>')
def route_video_details(id_title):
    """
    Lists details for the given title.
    """

    result = video_dal_retriever.retrieve_details(id_title)
    return jsonify({'details' : result})

@video.route('/video/languages')
def route_video_languages():
    """
    Lists each language that is stored for any of the videos.
    """

    result = video_dal_retriever.retrieve_languages()
    return jsonify({'languages' : result})

@video.route('/video/player/play', methods=['GET'])
def route_video_player_play():
    """
    Plays the video file given by ID (with the subtitle provided optionally).
    """

    return video_player_adapter.play_from_arguments(request.args)

@video.route('/video/qualities')
def route_video_qualities():
    """
    Lists each quality that is stored for any of the videos.
    """

    result = video_dal_retriever.retrieve_qualities()
    return jsonify({'qualities' : result})

@video.route('/video/titles')
def route_video_titles():
    """
    Lists all available titles.
    """

    result = _retrieve_titles(request.args)
    return jsonify({'titles' : result})

########################################################################################################################
# Private methods.
########################################################################################################################

def _retrieve_titles(filters):

    if filters is None or len(filters) <= 0:
        return video_dal_retriever.retrieve_titles()

    video_title_filter = VideoTitleFilter()

    if 'language' in filters:
        video_title_filter.language_id = filters['language']
    if 'parent' in filters:
        video_title_filter.parent_id = filters['parent']
    if 'quality' in filters:
        video_title_filter.quality_id = filters['quality']
    if 'subtitle' in filters:
        video_title_filter.subtitle_language_id = filters['subtitle']
    if 'text' in filters:
        video_title_filter.text = filters['text']

    return video_dal_retriever.retrieve_titles(video_title_filter)
