class PlayerHandler(object):
    """
    Interface that describes how a player handler should look like.
    """

    def faster(self):
        """
        Increases the speed of playing.
        """
        pass

    def fast_forward(self):
        """
        Jumps 10 minutes forward in time.
        """
        pass

    def fast_rewind(self):
        """
        Jumps 10 minutes back in time.
        """
        pass

    def forward(self):
        """
        Jumps half a minute forward in time.
        """
        pass

    def pause(self):
        """
        Pauses the player.
        """
        pass

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
        pass

    def rewind(self):
        """
        Jumps half a minute back in time.
        """
        pass

    def slower(self):
        """
        Decreases the speed of playing.
        """
        pass

    def stop(self):
        """
        Stops the player and make it exit.
        """
        pass

    def volume_down(self):
        """
        Decreases the volume.
        """
        pass

    def volume_up(self):
        """
        Increases the volume.
        """
        pass
