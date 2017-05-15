import atexit
import os
import subprocess

from multimedia.functions import terminate_process

class FehImageViewerHandler(object):
    """
    Interface for feh image viewer which is an X11 application that can be started from the command line. It is
    controlled by sending spoofed keystrokes through xdotool.

    feh only works if the application is started from an X11 session.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, binary_path=None):

        ### Private attributes.
        # The path of the executable.
        if binary_path is None:
            self._binary = '/usr/bin/feh'
        else:
            self._binary = binary_path
        # A handle to the running player process.
        self._current_process = None
        self._xdotool_binary = 'xdotool'

    ####################################################################################################################
    # ImageViewerHandler implementation.
    ####################################################################################################################

    def next(self):
        """
        Shows the next image.
        """

        self._send_keystroke("Right")
        return True

    def previous(self):
        """
        Shows the previous image.
        """

        self._send_keystroke("Left")
        return True

    def stop(self):
        """
        Exits the viewer.
        """

        self._send_keystroke("q")
        result = terminate_process(self._current_process)
        self._current_process = None

        return result

    def view(self, files):
        """
        Shows the given images.
        """

        # Stop viewer if it is running.
        self.stop()

        # Construct command to execute.
        program = [self._binary, '-FZ', os.path.split(files[0])[0]]

        # Execute command.
        self._current_process = subprocess.Popen(program)
        atexit.register(self.stop)

        return True

    def zoom_in(self):
        """
        Shows the next image.
        """

        self._send_keystroke("Up")
        return True

    def zoom_out(self):
        """
        Shows the previous image.
        """

        self._send_keystroke("Down")
        return True

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _send_keystroke(self, key):
        """
        Shows the previous image.
        """

        subprocess.call([self._xdotool_binary, "key", key])
