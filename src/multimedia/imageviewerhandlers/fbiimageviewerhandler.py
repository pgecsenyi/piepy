import atexit
import subprocess

from multimedia.functions import terminate_process

class FbiImageViewerHandler(object):
    """
    Interface for fbi (Linux Frame Buffer Image Viewer) which is a command line application that uses Linux Frame Buffer
    to display images.

    fbi only works if the application is started from a Linux console (/dev/ttyN), a pseudo tty (xterm, ssh, screen,
    etc.) will not work. Therefore we are also not able to control it through a custom pipe.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, binary_path=None):

        ### Private attributes.
        # The path of the executable.
        if binary_path is None:
            self._binary = '/usr/bin/fbi'
        else:
            self._binary = binary_path
        # A handle to the running player process.
        self._current_process = None

    ####################################################################################################################
    # ImageViewerHandler implementation.
    ####################################################################################################################

    def next(self):
        """
        Shows the next image.
        """

        # return send_keytroke_to_process(self._current_process, KEY_PAGE_DOWN)
        return False

    def previous(self):
        """
        Shows the previous image.
        """

        # return send_keytroke_to_process(self._current_process, KEY_PAGE_UP)
        return False

    def stop(self):
        """
        Exits the viewer.
        """

        # result = exit_process_send_keystroke(self._current_process, 'q')
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
        program = [self._binary, '-a', ' '.join(files)]

        # Execute command.
        self._current_process = subprocess.Popen(program)
        atexit.register(self.stop)

        return True

    def zoom_in(self):
        """
        Shows the next image.
        """

        # return send_keytroke_to_process(self._current_process, '+')
        return False

    def zoom_out(self):
        """
        Shows the previous image.
        """

        # return send_keytroke_to_process(self._current_process, '-')
        return False
