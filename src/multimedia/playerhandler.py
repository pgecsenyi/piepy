class PlayerHandler:
    """
    Interface that describes how a player handler should look like.
    """

    def faster(self):
        """
        Increases the speed of playing.
        """

    def fast_forward(self):
        """
        Jumps 10 minutes forward in time.
        """

    def fast_rewind(self):
        """
        Jumps 10 minutes back in time.
        """

    def forward(self):
        """
        Jumps half a minute forward in time.
        """

    def pause(self):
        """
        Pauses the player.
        """

    def play(self, audio_output, file_to_play, subtitle_to_use=None, on_exit=None):
        """
        Starts playing the given file with an optional subtitle.

        Parameters
        ----------
        audio_output : int
            Defines which audio output to use.
        file_to_play : str
            The path of the file to play.
        subtitle_to_use : str
            The path of the subtitle to use.
        on_exit : object
            A callback method that is called when the process exited.
        """

    def rewind(self):
        """
        Jumps half a minute back in time.
        """

    def slower(self):
        """
        Decreases the speed of playing.
        """

    def stop(self):
        """
        Stops the player and make it exit.
        """

    def volume_down(self):
        """
        Decreases the volume.
        """

    def volume_up(self):
        """
        Increases the volume.
        """
