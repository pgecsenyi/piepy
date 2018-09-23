"""
Config

Data structure to store configuration.
"""

from dal.configuration.tags import get_complete_tag, TAG_ALBUM, TAG_ANY, TAG_ARTIST, TAG_EPISODE_TITLE, TAG_LANGUAGE, \
                                   TAG_LANGUAGES, TAG_NUMBER, TAG_QUALITY, TAG_TITLE

class Config(object):
    """
    Stores application settings.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.database = DatabaseConfig()
        self.indexing = IndexingConfig()
        self.logging = LoggingConfig()
        self.multimedia = MultimediaConfig()
        self.web = WebConfig()

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def create_default(self):
        """
        Generates a sample configuration.
        """

        self.database.lifetime = 604800
        self.database.path_media = '../data/media.db'
        self.database.path_playlist = '../data/playlist.db'
        self.indexing.audio.rules = [IndexerRuleConfig()]
        self.indexing.audio.rules[0].directory = '/mnt/hdd/Audio'
        self.indexing.audio.rules[0].extensions = ['.flac', '.mp3', '.ogg', '.wav']
        self.indexing.audio.rules[0].pattern = '{}/{}/{} {}'.format(
            get_complete_tag(TAG_ARTIST),
            get_complete_tag(TAG_ALBUM),
            get_complete_tag(TAG_NUMBER),
            get_complete_tag(TAG_TITLE))
        self.indexing.image.rules = [IndexerRuleConfig()]
        self.indexing.image.rules[0].directory = '/mnt/hdd/Image'
        self.indexing.image.rules[0].extensions = ['.gif', '.jpg', '.jpeg', '.png']
        self.indexing.image.rules[0].pattern = '{}/{}'.format(
            get_complete_tag(TAG_ALBUM),
            get_complete_tag(TAG_TITLE))
        self.indexing.video.ignore_revisions = False
        self.indexing.video.subtitle_rules = [IndexerRuleConfig()]
        self.indexing.video.subtitle_rules[0].directory = '/mnt/hdd/Video'
        self.indexing.video.subtitle_rules[0].extensions = ['.srt']
        self.indexing.video.subtitle_rules[0].pattern = '{}/Subtitle/{}/{}/{}/{}/{}'.format(
            get_complete_tag(TAG_TITLE),
            get_complete_tag(TAG_QUALITY),
            get_complete_tag(TAG_LANGUAGES),
            get_complete_tag(TAG_LANGUAGE),
            get_complete_tag(TAG_ANY),
            get_complete_tag(TAG_EPISODE_TITLE))
        self.indexing.video.video_rules = [IndexerRuleConfig()]
        self.indexing.video.video_rules[0].directory = '/mnt/hdd/Video'
        self.indexing.video.video_rules[0].extensions = ['.avi', '.flv', '.mkv', '.mp4']
        self.indexing.video.video_rules[0].pattern = '{}/Content/{}/{}/{}/{}'.format(
            get_complete_tag(TAG_TITLE),
            get_complete_tag(TAG_QUALITY),
            get_complete_tag(TAG_LANGUAGES),
            get_complete_tag(TAG_ANY),
            get_complete_tag(TAG_EPISODE_TITLE))
        self.logging.enabled = True
        self.logging.level = 'error'
        self.logging.max_size_bytes = 524288
        self.logging.path = '../data/log.txt'
        self.multimedia.av_player = 'vlc'
        self.multimedia.av_player_path = '/usr/bin/vlc-wrapper'
        self.multimedia.image_viewer = 'feh'
        self.multimedia.image_viewer_path = '/usr/bin/feh'
        self.web.port = 8095

class DatabaseConfig(object):
    """
    Stores database related application settings.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.lifetime = 604800
        self.path_media = None
        self.path_playlist = None

class IndexerRuleConfig(object):
    """
    Stores the configuration parameters of an Indexer Rule.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.directory = None
        self.extensions = None
        self.pattern = None

class IndexingAudioConfig(object):
    """
    Stores settings related to audio indexing.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.rules = []

class IndexingConfig(object):
    """
    Stores settings related to indexing.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.audio = IndexingAudioConfig()
        self.image = IndexingImageConfig()
        self.video = IndexingVideoConfig()

class IndexingImageConfig(object):
    """
    Stores settings related to image indexing.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.rules = []

class IndexingVideoConfig(object):
    """
    Stores settings related to video indexing.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.ignore_revisions = False
        self.subtitle_rules = []
        self.video_rules = []

class LoggingConfig(object):
    """
    Stores logging configuration.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.enabled = True
        self.level = 'error'
        self.max_size_bytes = None
        self.path = None

class MultimediaConfig(object):
    """
    Stores multimedia related application settings.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.av_player = None
        self.av_player_path = None
        self.image_viewer = None
        self.image_viewer_path = None

class WebConfig(object):
    """
    Stores web related application settings.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.port = 8095
