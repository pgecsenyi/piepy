"""
Parses command line arguments.
"""

import getopt
import sys

from dal.configuration.config import Config
from dal.configuration.configmanager import ConfigManager

class ArgumentParser:
    """
    Parses command line arguments.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):
        """
        Initializes attributes.

        Parameters
        ----------
        arguments : list of str
            The list of the arguments.
        """

        self._application_name = ''
        self._arguments = sys.argv
        self._config_file_path = None
        self._default_config_file_path = 'config.json'
        self._is_debugging_enabled = False
        self._log_file_path = None

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def config_file_path(self) -> str:
        """
        Gets the path of the configuration file.
        """
        return self._config_file_path

    @property
    def is_debugging_enabled(self) -> bool:
        """
        Gets a value indicating whether debug mode is enabled.
        """
        return self._is_debugging_enabled

    @property
    def log_file_path(self) -> str:
        """
        Gets the path of the log file.
        """
        return self._log_file_path

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def parse_arguments(self):
        """
        Parses command line arguments, prints usage and generates configuration file if necessary.
        """

        is_config_generation_requested = False
        self._application_name, parameters = self._arguments[0], self._arguments[1:]

        try:
            opts, _ = getopt.getopt(parameters, 'c:dhil:', ['config=', 'debug', 'help', 'install', 'log'])
        except getopt.GetoptError:
            self._print_usage_and_exit(2)

        for opt, arg in opts:
            if opt in ('-c', '--config'):
                self._config_file_path = arg
            elif opt in ('-d', '--debug'):
                self._is_debugging_enabled = True
            elif opt in ('-h', '--help'):
                self._print_usage_and_exit()
            elif opt in ('-i', '--install'):
                is_config_generation_requested = True
            elif opt in ('-l', '--log'):
                self._log_file_path = arg

        if is_config_generation_requested:
            self._generate_config_and_exit()

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _print_usage_and_exit(self, error_code=0):
        """
        Prints a short manual and exists the application.

        Parameters
        ----------
        error_code : int
            The error code to exit with.
        """

        print('python {0} <options>'.format(self._application_name))
        print('')
        print('  -c, --config    Use the specified configuration file instead')
        print('                  of the default ({0}) one.'.format(self._default_config_file_path))
        print('  -d, --debug     Run the application in debug mode.')
        print('  -h, --help      Print this help and exit.')
        print('  -i, --install   Generate a sample configuration file and exit.')
        print('  -l, --log       Log to the specified file.')
        print('')
        print(
            'Run the application as a member of the \'video\' group. In case you would like to use port 80, run the '
            'application as superuser.')
        sys.exit(error_code)

    def _generate_config_and_exit(self):
        """
        Generates a default configuration file and exists the application.
        """

        config = Config()
        config.create_default()
        ConfigManager.save(self._config_file_path, config)

        print('Configuration file successfully generated to {0}.'.format(self._config_file_path))
        sys.exit(0)
