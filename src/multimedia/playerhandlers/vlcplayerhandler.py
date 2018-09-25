import atexit
import errno
import os
import socket
import subprocess

from multimedia.functions import popen_and_wait_for_exit, terminate_process
from multimedia.playerhandler import PlayerHandler

class VlcPlayerHandler(PlayerHandler):
    """
    Interface for VLC player which is an X11 application that can be started from the command line. It is controlled
    using a UNIX Domain Socket (UDS). The application tries to enable VLC's socket interface automatically, but in case
    it fails you can also do it manually under 'Preferences / Interfaces / Main interfaces / Remote control interface'
    and can be configured under 'Preferences / Interfaces / Main interfaces / RC'. Set the path of the socket to the
    same as the '_socket_for_player' attribute's value.

    Use 'vlc-wrapper' binary instead of 'vlc' if you would like to run the server application as root. Note however that
    running the app as root is not recommended (but of course it's necessary if port 80 is used).
    """

    ####################################################################################################################
    # Private static attributes.
    ####################################################################################################################

    # Indicates how many instances are created of this class (needed to be able to create a new socket for each new
    # player process).
    _instance_count = 0

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, binary_path=None):

        ### Private attributes.
        # The path of the executable.
        if binary_path is None:
            self._binary = '/usr/bin/vlc-wrapper'
        else:
            self._binary = binary_path
        # A handle to the running player process.
        self._current_process = None
        # The playlist.
        self._playlist = {}
        # A reference to the socket through which communication with VLC is performed.
        self._socket = None
        # The path of the socket.
        self._socket_for_player = '/tmp/vlc' + str(VlcPlayerHandler._instance_count) + '.sock'

        # Increase instance counter.
        VlcPlayerHandler._instance_count = VlcPlayerHandler._instance_count + 1

    ####################################################################################################################
    # "PlayerHandler" implementation.
    ####################################################################################################################

    def faster(self):

        return self._send_simple_command('faster')

    def fast_forward(self):

        return self._seek(600)

    def fast_rewind(self):

        return self._seek(-600)

    def forward(self):

        return self._seek(30)

    def pause(self):
        """
        Sends pause command to VLC using it's UDS.
        """

        return self._send_simple_command('pause')

    def play(self, audio_output, file_to_play, subtitle_to_use=None, on_exit=None):
        """
        Start playing the specified file using the optionally specified subtitle.
        """

        # Stop previous playing.
        self.stop()

        # Make sure the socket does not exist already.
        try:
            os.unlink(self._socket_for_player)
        except OSError:
            if os.path.exists(self._socket_for_player):
                return False

        # Display it on the default display (this can be handled by VLC, using the appropriate command line argument).
        # os.environ['DISPLAY'] = ':0'

        # Prepare command.
        program = self._prepare_process_arguments(file_to_play, subtitle_to_use)

        # Execute command.
        if on_exit is None:
            self._current_process = subprocess.Popen(program)
        else:
            program.append('--play-and-exit')
            popen_and_wait_for_exit(False, on_exit, self._set_process, program)

        atexit.register(self.stop)

        return True

    def rewind(self):

        return self._seek(-30)

    def slower(self):

        return self._send_simple_command('slower')

    def stop(self):
        """
        Sends stop and quit commands to VLC using it's UDS, then kills the process if it is still exists.
        """

        # Nothing to do here.
        if self._current_process is None:
            return False

        # Try to exit cleanly.
        if self._connect() is True:
            try:
                self._socket.sendall('stop\n')
                self._socket.sendall('quit\n')
            except Exception:
                pass
            self._close()

        # Terminate process if it is still alive.
        result = terminate_process(self._current_process)
        self._current_process = None

        return result

    def volume_down(self):

        return self._send_simple_command('voldown 1')

    def volume_up(self):

        return self._send_simple_command('volup 1')

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def playlist_add(self, item_id, file_to_add):

        self._playlist[item_id] = file_to_add

        return self._send_simple_command('enqueue "{}"'.format(file_to_add.encode('utf-8')))

    def playlist_clear(self):

        self._playlist = {}

        return self._send_simple_command('clear')

    def playlist_remove(self, item_id):

        self._playlist.pop(item_id, None)
        if not self._send_simple_command('clear'):
            return False
        for file_to_add in self._playlist.items():
            self._send_simple_command('enqueue "{}"'.format(file_to_add.encode('utf-8')))

        return True

    ####################################################################################################################
    # Auxiliary methods -- Process management.
    ####################################################################################################################

    def _prepare_process_arguments(self, file_to_play, subtitle_to_use=None):

        # Construct command to execute. '--extraintf=oldrc' could be '-I oldrc'.
        program = [
            self._binary,
            '-f', '--no-osd', '--no-video-title-show',
            '--x11-display=:0',
            '--extraintf=oldrc', '--rc-unix=' + self._socket_for_player]
        program.append(file_to_play)

        # Append the subtitle-related part to the command if necessary.
        if subtitle_to_use is not None:
            program.append('--sub-file=' + subtitle_to_use)

        return program

    def _set_process(self, process):

        self._current_process = process

    ####################################################################################################################
    # Auxiliary methods -- Socket communication.
    ####################################################################################################################

    def _close(self):
        """
        Closes UDS.
        """

        if self._socket is not None:
            self._socket.close()
            self._socket = None

    def _connect(self):
        """
        Connects to VLC's UDS.
        """

        if self._socket is None:
            self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                self._socket.connect(self._socket_for_player)
            except socket.error:
                return False

        return True

    def _flush_socket(self):
        """
        Naive method for emptying a socket, because Python does not seem to support this by default.
        """

        if self._current_process is None:
            return False

        if self._connect() is False:
            return False

        try:
            self._socket.setblocking(0)

            # Seek fails for the first time dirty fix. This would be only necessary for the first flush call after
            # starting the process, but does not harm anyway.
            self._socket.sendall('\n')

            size = 1
            while size > 0:
                data = self._socket.recv(256)
                size = len(data)
        except socket.error as ex:
            if ex.errno == errno.EAGAIN:
                return True
            return False
        except Exception:
            return 0

        return True

    def _seek(self, time):
        """
        Positions head relative with the given time.
        """

        if self._current_process is None:
            return False

        if self._connect() is False:
            return False

        try:
            if not self._flush_socket():
                return False
            self._socket.setblocking(1)
            self._socket.sendall('get_time\n')
            response = self._socket.recv(16)
            self._socket.sendall('seek ' + str(int(response[:-2]) + time) + '\n')
        except Exception:
            return False

        return True

    def _send_simple_command(self, command):
        """
        Sends a simple command through the UDS.
        """

        if self._current_process is None:
            return False

        if self._connect() is False:
            return False

        try:
            self._socket.sendall(command + '\n')
        except Exception:
            return False

        return True
