from multimedia.playlist.entities import PlayingState

class PlaylistHandler(object):

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, player_handler):

        ### Validate parameters.
        if player_handler is None:
            raise Exception('player_handler cannot be None.')

        ### Attributes from the outside.
        # A default player handler that will be used if no suitable player handler is found for a given track.
        self._player_handler = player_handler

        ### Private attributes.
        # The ID of the track that is played currently.
        self._current_state = PlayingState(0, player_handler)
        # Indicates whether the playing is paused currently.
        self._is_paused = False
        # Indicates whether the playlist is played currently.
        self._is_playing = False
        # A dictionary containing label (str) => player (PlayerHandler) pairs.
        self._player_handlers = {}
        # The playlist -- a list of PlaylistTracks.
        self._playlist = []

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def add_track(self, track):
        """
        Adds the given track to the playlist.

        Parameters
        ----------
        track : PlaylistTrack
            The track to add.
        """

        self._playlist.append(track)

    def add_tracks(self, tracks):
        """
        Adds the given tracks to the playlist.

        Parameters
        ----------
        tracks : list of PlaylistTrack
            The tracks to add.
        """

        if tracks is None:
            return

        for track in tracks:
            self._playlist.append(track)

    def clear(self):
        """
        Clears the playlist.
        """

        self.stop()
        self._playlist = []

    def delete_track(self, track_id):
        """
        Removes the given track from the playlist.

        Parameters
        ----------
        track_id : int
            The ID of the track to remove from the playlist.
        """

        if track_id == self._current_state.track_id:
            self.stop()

        for i in range(0, len(self._playlist)):
            if self._playlist[i].track_id == track_id:
                del self._playlist[i]
                return True

        return False

    def next(self):

        self._play_next_track()

    def pause(self):

        if not self._is_playing:
            return False

        if self._current_state.player_handler != None:
            self._current_state.player_handler.pause()
            self._is_paused = not self._is_paused
            self._is_playing = not self._is_playing

    def play(self, track_id=None):
        """
        Plays the tracks from the playlist starting with the specified track.
        """

        if len(self._playlist) <= 0:
            return False
        if self._is_paused:
            self.pause()

        first_track = self._playlist[0]
        if track_id != None:
            first_track = self._get_track(track_id)
        if first_track is None:
            return False

        result = self._play_track(first_track)

        return result

    def previous(self):

        self._play_previous_track()

    def set_player_handler(self, label, player):
        """
        Sets the player which will be associated with playlist tracks having the same label.

        Parameters
        ----------
        label : str
            The label for the new player.
        player: PlayerHandler
            The player.
        """

        self._player_handlers[label] = player

    def stop(self):

        if not self._is_playing:
            return False

        self._is_paused = False
        self._is_playing = False

        result = self._player_handler.stop()
        for player_handler in self._player_handlers.values():
            result = player_handler.stop() or result

        return result

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _get_next_track(self, track_id):

        if len(self._playlist) <= 1:
            return None

        for i in range(0, len(self._playlist) - 1):
            if self._playlist[i].track_id == track_id:
                return self._playlist[i + 1]

        return None

    def _get_previous_track(self, track_id):

        if len(self._playlist) <= 1:
            return None

        previous = None
        for track in self._playlist:
            if track.track_id == track_id:
                return previous
            previous = track

        return previous

    def _get_track(self, track_id):

        for playlist_track in self._playlist:
            if playlist_track.track_id == track_id:
                return playlist_track

        return None

    def _play_next_track(self):

        if not self._is_playing:
            return False

        next_track = self._get_next_track(self._current_state.track_id)
        if next_track is None:
            return

        self._play_track(next_track)

    def _play_previous_track(self):

        if not self._is_playing:
            return False

        previous_track = self._get_previous_track(self._current_state.track_id)
        if previous_track is None:
            return

        self._play_track(previous_track)

    def _play_track(self, track):

        label = track.label
        player_handler = self._player_handler
        if label != None and label in self._player_handlers:
            player_handler = self._player_handlers[label]

        if player_handler != self._current_state.player_handler:
            self._current_state.player_handler.stop()
        self._current_state.track_id = track.track_id
        self._current_state.player_handler = player_handler

        self._is_playing = True

        return player_handler.play(track.audio_output, track.path, track.subtitle_path, self._play_next_track)
