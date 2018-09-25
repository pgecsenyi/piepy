from bll.playlist.entities import Playlist as PlaylistBll
from bll.playlist.entities import PlaylistHeader as PlaylistHeaderBll
from bll.playlist.entities import PlaylistTrack as PlaylistTrackBll
from dal.playlist.entities import NewPlaylist as NewPlaylistDal
from dal.playlist.entities import NewPlaylistTrack as NewPlaylistTrackDal
from dal.playlist.entities import PlaylistHeader as PlaylistHeaderDal
from dal.playlist.playlistdatahandler import PlaylistDataHandler
from multimedia.playlist.entities import PlaylistTrack as TrackMedia

class PlaylistManager:
    """
    Manages playlists, interacts with DAL and MULTIMEDIA modules.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, db_context, playlist_handler):

        ### Validate parameters.
        if db_context is None:
            raise Exception('db_context cannot be None.')
        if playlist_handler is None:
            raise Exception('playlist_handler cannot be None.')

        ### Attributes from the outside.
        self._playlist_handler = playlist_handler

        ### Private attributes.
        self._audio_retriever = None
        self._data_handler = PlaylistDataHandler(db_context)
        self._playlist = None
        self._video_retriever = None

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def audio_retriever(self):
        return self._audio_retriever

    @audio_retriever.setter
    def audio_retriever(self, value):
        self._audio_retriever = value

    @property
    def video_retriever(self):
        return self._video_retriever

    @video_retriever.setter
    def video_retriever(self, value):
        self._video_retriever = value

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def add_playlist(self, new_playlist):

        if new_playlist is None:
            return None

        new_playlist_dal = self._newplaylist_to_dal(new_playlist)
        new_playlist_id = self._data_handler.insert_playlist(new_playlist_dal)

        return PlaylistHeaderBll(new_playlist_id, new_playlist_dal.title)

    def add_track(self, playlist_id, new_track, number_after=0):

        if new_track is None:
            return None

        new_track_dal = self._newtrack_to_dal(new_track)
        new_track_id = self._data_handler.insert_track(playlist_id, new_track_dal, number_after)
        if new_track_id is None:
            return None

        return PlaylistTrackBll(
            new_track_id,
            new_track_dal.category,
            new_track_dal.title,
            new_track_dal.path,
            new_track_dal.audio_output)

    def create_db(self):

        self._data_handler.create_db()

    def delete_playlist(self, playlist_id):

        if playlist_id is None:
            return

        if (self._playlist is not None) and (playlist_id == self._playlist.playlist_id):
            self._playlist_handler.clear()

        self._data_handler.delete_playlist(playlist_id)

    def delete_track(self, track_id):

        if track_id is None:
            return
        if self._playlist_has_track(track_id):
            self._playlist_handler.delete_track(track_id)

        self._data_handler.delete_track(track_id)

    def move_track(self, playlist_id, number_to_move, number_after):

        if playlist_id is None:
            return

        self._data_handler.move_track(playlist_id, number_to_move, number_after)

    def next(self):

        self._playlist_handler.next()

    def pause(self):

        self._playlist_handler.pause()

    def play(self, playlist_id):

        if playlist_id is None:
            return False

        # Retrieve and cache playlist.
        playlist_dal = self._data_handler.retrieve_playlist(playlist_id)
        self._playlist = self._playlist_to_bll(playlist_dal)

        # Pass it's tracks to the media module.
        tracks_media = self._tracks_to_media(self._playlist.tracks)
        self._playlist_handler.add_tracks(tracks_media)
        result = self._playlist_handler.play()

        return result

    def previous(self):

        self._playlist_handler.previous()

    def retrieve_playlist(self, playlist_id=None):

        if playlist_id is None:
            return self._playlist

        playlist_dal = self._data_handler.retrieve_playlist(playlist_id)
        playlist_bll = self._playlist_to_bll(playlist_dal)

        return playlist_bll

    def retrieve_playlist_headers(self):

        playlist_headers_dal = self._data_handler.retrieve_playlist_headers()
        playlist_headers_bll = self._playlist_headers_to_bll(playlist_headers_dal)

        return playlist_headers_bll

    def stop(self):

        return self._playlist_handler.stop()

    def update_playlist(self, playlist_header):

        if playlist_header is None:
            return

        playlist_header_dal = self._playlist_header_to_dal(playlist_header)
        self._data_handler.update_playlist(playlist_header_dal)

    ####################################################################################################################
    # Private methods -- conversion.
    ####################################################################################################################

    def _newplaylist_to_dal(self, new_playlist_bll):

        if new_playlist_bll is None:
            return None

        tracks_dal = self._newtracks_to_dal(new_playlist_bll.tracks)
        new_playlist_dal = NewPlaylistDal(new_playlist_bll.title, tracks_dal)

        return new_playlist_dal

    def _newtrack_to_dal(self, new_track_bll):

        if new_track_bll is None:
            return None

        title, path = self._retrieve_file_data(new_track_bll.category, new_track_bll.file_id)
        if (title is None) or (path is None):
            return None

        track_dal = NewPlaylistTrackDal(new_track_bll.category, title, path, new_track_bll.audio_output)

        return track_dal

    def _newtracks_to_dal(self, new_tracks_bll):

        tracks_dal = []
        if new_tracks_bll is None:
            return tracks_dal

        for new_track_bll in new_tracks_bll:
            track_dal = self._newtrack_to_dal(new_track_bll)
            if track_dal is not None:
                tracks_dal.append(track_dal)

        return tracks_dal

    def _playlist_header_to_bll(self, playlist_header_dal):

        if playlist_header_dal is None:
            return None

        playlist_header_bll = PlaylistHeaderBll(playlist_header_dal.playlist_id, playlist_header_dal.title)

        return playlist_header_bll

    def _playlist_header_to_dal(self, playlist_header_bll):

        if playlist_header_bll is None:
            return None

        playlist_header_dal = PlaylistHeaderDal(playlist_header_bll.playlist_id, playlist_header_bll.title)

        return playlist_header_dal

    def _playlist_headers_to_bll(self, playlist_headers_dal):

        if playlist_headers_dal is None:
            return None

        playlist_headers_bll = []
        for playlist_header_dal in playlist_headers_dal:
            playlist_header_bll = self._playlist_header_to_bll(playlist_header_dal)
            playlist_headers_bll.append(playlist_header_bll)

        return playlist_headers_bll

    def _playlist_to_bll(self, playlist_dal):

        if playlist_dal is None:
            return None

        tracks_bll = self._tracks_to_bll(playlist_dal.tracks)
        playlist_bll = PlaylistBll(playlist_dal.playlist_id, playlist_dal.title, tracks_bll)

        return playlist_bll

    def _track_to_bll(self, track_dal):

        if track_dal is None:
            return None

        track_bll = PlaylistTrackBll(
            track_dal.track_id, track_dal.category, track_dal.title, track_dal.path, track_dal.audio_output)

        return track_bll

    def _tracks_to_bll(self, tracks_dal):

        tracks_bll = []
        if tracks_dal is None:
            return tracks_bll

        for track_dal in tracks_dal:
            track_bll = self._track_to_bll(track_dal)
            if track_bll is not None:
                tracks_bll.append(track_bll)

        return tracks_bll

    def _tracks_to_media(self, tracks_bll):

        tracks_media = []
        if tracks_bll is None:
            return tracks_media

        for track_bll in tracks_bll:
            track_media = TrackMedia(track_bll.track_id, track_bll.path, None)
            tracks_media.append(track_media)

        return tracks_media

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _playlist_has_track(self, track_id):

        if self._playlist is None or self._playlist.tracks is None:
            return False

        for track in self._playlist.tracks:
            if track.track_id == track_id:
                return True

        return False

    def _retrieve_file_data(self, category, file_id):

        if category == 'audio':
            if self._audio_retriever is None:
                return None
            return self.audio_retriever.retrieve_file_data(file_id)
        if category == 'video':
            if self._video_retriever is None:
                return None
            return self.video_retriever.retrieve_file_data(file_id)

        return None
