class NewPlaylist(object):
    """
    Represents a new playlist, which is about to be stored.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, title, tracks):
        """
        Initializes attributes.

        Parameters
        ----------
        title : str
            The title of the playlist.
        tracks : list of NewPlaylistTrack
            The tracks of playlist.
        """

        ### Validate parameters.
        if title is None:
            raise Exception('title cannot be None.')
        if tracks is None:
            raise Exception('tracks cannot be None.')

        ### Attributes from outside.
        self._title = title
        self._tracks = tracks

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def title(self):
        return self._title

    @property
    def tracks(self):
        return self._tracks

class NewPlaylistTrack(object):
    """
    Represents a track on a new playlist.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, category, file_id):
        """
        Initializes attributes.

        Parameters
        ----------
        category : str
            The category that has the corresponding file.
        file_id : int
            The ID of the corresponding file.
        """

        ### Attributes from outside.
        self._category = category
        self._file_id = file_id

        ### Private attributes.
        self._audio_output = 0

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def audio_output(self):
        """
        Gets the chosen audio output for this track.
        """
        return self._audio_output

    @audio_output.setter
    def audio_output(self, value):
        """
        Sets the audio output for this track.
        """
        if value < 0:
            self._audio_output = 0
        else:
            self._audio_output = value

    @property
    def category(self):
        return self._category

    @property
    def file_id(self):
        return self._file_id

class Playlist(object):
    """
    Represents a playlist.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, playlist_id, title, tracks):

        ### Validate parameters.
        if title is None:
            raise Exception('title cannot be None.')
        if tracks is None:
            raise Exception('tracks cannot be None.')

        ### Attributes from outside.
        self._playlist_id = playlist_id
        self._title = title
        self._tracks = tracks

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def title(self):
        return self._title

    @property
    def tracks(self):
        return self._tracks

class PlaylistHeader(object):
    """
    Stores the ID and the title of a playlist without the tracks.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, playlist_id, title):

        ### Validate parameters.
        if playlist_id is None:
            raise Exception('playlist_id cannot be None.')
        if title is None:
            raise Exception('title cannot be None.')

        ### Attributes from outside.
        self._playlist_id = playlist_id
        self._title = title

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def title(self):
        return self._title

class PlaylistTrack(object):
    """
    Represents a track of a playlist.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, track_id, category, title, path, audio_output):
        """
        Initializes attributes.

        Parameters
        ----------
        track_id : int
            The ID of the track.
        category : str
            The category of the file this track represents.
        title : str
            The title of the track.
        path : str
            The path of the file.
        audio_output : int
            A number indicating the chosen audio output for this track.
        """

        ### Attributes from outside.
        self._track_id = track_id
        self._category = category
        self._title = title
        self._path = path
        self._audio_output = audio_output

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def audio_output(self):
        """
        Gets the chosen audio output for this track.
        """
        return self._audio_output

    @property
    def category(self):
        return self._category

    @property
    def path(self):
        return self._path

    @property
    def title(self):
        return self._title

    @property
    def track_id(self):
        return self._track_id
