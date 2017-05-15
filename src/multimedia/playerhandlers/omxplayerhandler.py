import atexit
import subprocess

from multimedia.constants import AUDIO_OUTPUT_ANALOG, KEY_DOWN_ARROW, KEY_LEFT_ARROW, KEY_RIGHT_ARROW, KEY_UP_ARROW
from multimedia.functions import exit_process_send_keystroke, popen_and_wait_for_exit, send_keytroke_to_process
from multimedia.playerhandler import PlayerHandler

class OmxPlayerHandler(PlayerHandler):
    """
    Interface for omxplayer which is a command line application installed on Raspberry Pi by default that uses Linux
    Frame Buffer to display video files. It is controlled by sending spoofed keystrokes to the standard input.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, binary_path=None):

        ### Private attributes.
        # The path of the executable.
        if binary_path is None:
            self._binary = '/usr/bin/omxplayer'
        else:
            self._binary = binary_path
        # A handle to the running player process.
        self._current_process = None

    ####################################################################################################################
    # "PlayerHandler" implementation.
    ####################################################################################################################

    def faster(self):

        return send_keytroke_to_process(self._current_process, '2')

    def fast_forward(self):

        return send_keytroke_to_process(self._current_process, KEY_UP_ARROW)

    def fast_rewind(self):

        return send_keytroke_to_process(self._current_process, KEY_DOWN_ARROW)

    def forward(self):

        return send_keytroke_to_process(self._current_process, KEY_RIGHT_ARROW)

    def pause(self):
        """
        Simulates keypress used for pausing omxplayer.
        """

        return send_keytroke_to_process(self._current_process, ' ')

    def play(self, audio_output, file_to_play, subtitle_to_use=None, on_exit=None):
        """
        Start playing the specified file using the given audio output and the optionally specified subtitle.
        """

        # Stop previous playing.
        self.stop()

        # Prepare command.
        program = self._prepare_process_arguments(audio_output, file_to_play, subtitle_to_use)

        # Execute command.
        if on_exit is None:
            self._current_process = subprocess.Popen(
                program,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        else:
            popen_and_wait_for_exit(True, on_exit, self._set_process, program)

        atexit.register(self.stop)

        return True

    def rewind(self):

        return send_keytroke_to_process(self._current_process, KEY_LEFT_ARROW)

    def slower(self):

        return send_keytroke_to_process(self._current_process, '1')

    def stop(self):
        """
        Simulates keypress used for quitting omxplayer, then kills the process if it is still exists.
        """

        result = exit_process_send_keystroke(self._current_process, 'q')
        self._current_process = None

        return result

    def volume_down(self):

        return send_keytroke_to_process(self._current_process, '-')

    def volume_up(self):

        return send_keytroke_to_process(self._current_process, '+')

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _prepare_process_arguments(self, audio_output, file_to_play, subtitle_to_use=None):

        # Construct command to execute.
        program = [self._binary, file_to_play]

        # Use different output if needed.
        if audio_output == AUDIO_OUTPUT_ANALOG:
            program.append('-o')
            program.append('local')
        # The else branch is somewhat redundant, because this is the default behavior.
        else:
            program.append('-o')
            program.append('hdmi')

        # Append the subtitle-related part to the command if necessary.
        if subtitle_to_use != None:
            program.append('--subtitles')
            program.append(subtitle_to_use)

        return program

    def _set_process(self, process):

        self._current_process = process
