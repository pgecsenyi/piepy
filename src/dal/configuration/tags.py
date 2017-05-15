"""
Tags.

Defines the tags that can be used for describing path patterns.
"""

########################################################################################################################
# Constants.
########################################################################################################################

# General.
TAG_ANY = 'any'
TAG_END_SEPARATOR = '%'
TAG_START_SEPARATOR = '%'

# Common.
TAG_TITLE = 'title'

# Audio.
TAG_ARTIST = 'artist'
TAG_NUMBER = 'number'

# Audio and image.
TAG_ALBUM = 'album'

# Video.
TAG_EPISODE_TITLE = 'episode_title'
TAG_LANGUAGE = 'language'
TAG_LANGUAGES = 'languages'
TAG_QUALITY = 'quality'

# Patterns.
TAG_ANY_PATTERN = '[^/]+'
TAG_FILENAME_PATTERN = '([^/]+)'
AUDIO_TAG_PATTERNS = {
    TAG_ALBUM : TAG_FILENAME_PATTERN,
    TAG_ARTIST : TAG_FILENAME_PATTERN,
    TAG_NUMBER : '([0-9]+)',
    TAG_TITLE : TAG_FILENAME_PATTERN}
IMAGE_TAG_PATTERNS = {
    TAG_ALBUM : TAG_FILENAME_PATTERN,
    TAG_TITLE : TAG_FILENAME_PATTERN}
SUBTITLE_TAG_PATTERNS = {
    TAG_EPISODE_TITLE : TAG_FILENAME_PATTERN,
    TAG_LANGUAGE : TAG_FILENAME_PATTERN,
    TAG_LANGUAGES : TAG_FILENAME_PATTERN,
    TAG_QUALITY : TAG_FILENAME_PATTERN,
    TAG_TITLE : TAG_FILENAME_PATTERN}
VIDEO_TAG_PATTERNS = {
    TAG_EPISODE_TITLE : TAG_FILENAME_PATTERN,
    TAG_LANGUAGES : TAG_FILENAME_PATTERN,
    TAG_QUALITY : TAG_FILENAME_PATTERN,
    TAG_TITLE : TAG_FILENAME_PATTERN}

########################################################################################################################
# Functions.
########################################################################################################################

def get_complete_tag(inner_tag):
    """
    Returns the complete tag (including separators) for the given inner tag.

    Parameters
    ----------
    inner_tag : str
        The inner part of the tag.
    """

    return TAG_START_SEPARATOR + inner_tag + TAG_END_SEPARATOR
