from os import path

from flask import Blueprint
from flask import jsonify

########################################################################################################################
# Initialization.
########################################################################################################################

image = Blueprint('image', __name__) # pylint: disable=invalid-name

image_dal = None # pylint: disable=invalid-name

image_viewer = None # pylint: disable=invalid-name

########################################################################################################################
# Routing.
########################################################################################################################

@image.route('/image/albums')
def route_image_albums():
    """
    Displays image albums
    """

    result = image_dal.retriever.retrieve_albums()
    return jsonify({'albums' : result})

@image.route('/image/viewer/next')
def route_image_next():
    """
    Shows the next image.
    """

    result = image_viewer.next()
    return jsonify({'next' : result})

@image.route('/image/viewer/previous')
def route_image_previous():
    """
    Shows the previous image.
    """

    result = image_viewer.previous()
    return jsonify({'previous' : result})

@image.route('/image/viewer/stop')
def route_image_stop():
    """
    Exits the viewer.
    """

    result = image_viewer.stop()
    return jsonify({'stop' : result})

@image.route('/image/viewer/view/<int:id_album>')
def route_image_view(id_album):
    """
    Returns an empty page.

    Returns
    -------
    An empty string.
    """

    files_with_ids = image_dal.retriever.retrieve_paths(id_album)

    # Check if the given files exist.
    if files_with_ids is None or not files_with_ids:
        return False

    existing_files = []
    for id_and_path in files_with_ids:
        if path.exists(id_and_path['path']):
            existing_files.append(id_and_path['path'])

    if not existing_files:
        return False

    # View.
    result = image_viewer.view(existing_files)

    return jsonify({'view' : result})

@image.route('/image/viewer/zoom-in')
def route_image_zoom_in():
    """
    Zooms in.
    """

    result = image_viewer.zoom_in()
    return jsonify({'zoom-in' : result})

@image.route('/image/viewer/zoom-out')
def route_image_zoom_out():
    """
    Zooms out.
    """

    result = image_viewer.zoom_out()
    return jsonify({'zoom-out' : result})
