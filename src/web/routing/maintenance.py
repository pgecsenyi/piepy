import datetime
from flask import Blueprint
from flask import jsonify

from bll.mediacatalog.catalogizer import Catalogizer
from dal.configuration.configmanager import ConfigManager
from dal.video.videotitlefilter import VideoTitleFilter
from web.util.deltatemplate import strfdelta

########################################################################################################################
# Initialization.
########################################################################################################################

catalogizer = None # pylint: disable=invalid-name

maintenance = Blueprint('maintenance', __name__) # pylint: disable=invalid-name

status_info = None # pylint: disable=invalid-name

status_info_tmp = {} # pylint: disable=invalid-name

video_dal_retriever = None # pylint: disable=invalid-name

########################################################################################################################
# Routing.
########################################################################################################################

@maintenance.route('/')
def route_home():
    """
    Returns an empty page.

    Returns
    -------
    An empty string.
    """

    return ''

@maintenance.route('/categories')
def route_categories():
    """
    Lists categories.

    Returns
    -------
    An array containing the loaded categories.
    """

    return jsonify({'categories' : ConfigManager.categories})

@maintenance.route('/rebuild')
def route_rebuild():
    """
    Rebuilds media database.

    Returns
    -------
    A JSON string describing the status of the rebuilding process.
    """

    status_info_tmp['last_sync_start'] = datetime.datetime.now()
    result = _get_status_string(catalogizer.rebuild_database_async(_on_synchronization_finished))

    return jsonify({'rebuild' : result})

@maintenance.route('/search/<string:search_string>', methods=['GET'])
def route_search(search_string):
    """
    Searches through titles.

    Parameters
    ----------
    search_string : str
        The search string.

    Returns
    -------
    A JSON string that contains a list of the found titles grouped by categories.
    """

    result = _search_video_titles(search_string)

    return jsonify({'videos' : result})

@maintenance.route('/status')
def route_status():
    """
    Returns the status of the synchronization process.

    Returns
    -------
    A JSON string describing the status of the synchronization process.
    """

    status_info.refresh()

    last_sync_duration = '0'
    if status_info.last_sync_duration is not None:
        last_sync_duration = strfdelta(status_info.last_sync_duration, '%M minutes %S seconds')
    last_sync_time = 'not performed'
    if status_info.last_sync_time is not None:
        last_sync_time = str(status_info.last_sync_time)

    result = {
        'number of audio files': status_info.audio_count,
        'number of image files': status_info.image_count,
        'number of video files': status_info.video_count,
        'synchronization' : _get_status_string(catalogizer.status),
        'duration of last synchronization' : last_sync_duration,
        'time of last synchronization' : last_sync_time,
        'uptime' : strfdelta(status_info.uptime, '%D days %H hours %M minutes %S seconds')}

    return jsonify({'status' : result})

@maintenance.route('/sync')
def route_sync():
    """
    Synchronizes database (looks for the changes only).

    Returns
    -------
    A JSON string describing the status of the synchronization process.
    """

    status_info_tmp['last_sync_start'] = datetime.datetime.now()
    result = _get_status_string(catalogizer.synchronize_database_async(_on_synchronization_finished))

    return jsonify({'sync' : result})

########################################################################################################################
# Private methods.
########################################################################################################################

def _get_status_string(status):

    if status == Catalogizer.STATUS_COMPLETED:
        return "completed"
    elif status == Catalogizer.STATUS_IN_PROGRESS:
        return "in progress"
    elif status == Catalogizer.STATUS_NOT_RUNNING:
        return "not running"
    elif status == Catalogizer.STATUS_STARTED:
        return "started"
    else:
        return "unknown"

def _on_synchronization_finished(status):

    if status == Catalogizer.STATUS_COMPLETED:

        now = datetime.datetime.now()
        status_info.last_sync_time = now

        last_sync_start = status_info_tmp['last_sync_start']
        if last_sync_start is not None:
            status_info.last_sync_duration = now - last_sync_start

def _search_video_titles(search_string):

    video_title_filter = VideoTitleFilter()
    video_title_filter.any_parent = True
    video_title_filter.text = search_string

    return video_dal_retriever.retrieve_titles(video_title_filter)
