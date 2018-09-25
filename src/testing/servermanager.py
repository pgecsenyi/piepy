import subprocess
import time

import requests

class ServerManager:

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, executable_path, config_path):

        ### Attributes from outside.
        self._executable_path = executable_path
        self._config_path = config_path

        ### Private attributes.
        self._current_process = None

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def start(self):

        self._current_process = subprocess.Popen(
            ['pipenv', 'run', 'python', self._executable_path, '-c', self._config_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    def stop(self):

        if self._current_process is not None:
            self._current_process.terminate()
            self._current_process.wait()
            self._current_process = None

    def wait_for_initialization(self, base_url):

        for _ in range(0, 10):
            time.sleep(1)
            response = requests.get(base_url)
            if response.status_code == 200:
                return True

        return False
