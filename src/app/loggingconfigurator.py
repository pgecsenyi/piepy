"""
Implements logging configurator logic.
"""

import logging
import logging.handlers

from dal.configuration.configmanager import ConfigManager

class LoggingConfigurator(object):
    """
    Implements logging configurator logic.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, is_debugging_enabled: bool = False, log_path_override: str = None):
        """
        Initializes attributes.

        Parameters
        ----------
        is_debugging_enabled : boolean
            Indicates whether the application is running in debug mode.
        log_path_override : str
            The path of the log file to use. If set to None, then the application will use the path provided in the
            configuration file.
        """

        self._is_debugging_enabled = is_debugging_enabled
        self._log_path_override = log_path_override

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def configure_logging(self):
        """
        Configures logging based on the provided parameters: enables or disables logging into a file or to the console
        and sets the debug level as well. Makes use of Python's built-in logging module.
        """

        logger = logging.getLogger()

        logging_config = ConfigManager.settings.logging
        log_level = self._determine_log_level()
        log_path = self._determine_log_path()
        is_logging_possible = logging_config.enabled and (log_path is not None) and (logging_config.max_size_bytes > 0)

        logger.setLevel(log_level)

        # If debugging is enabled, log to the command line on DEBUG level by all means.
        if self._is_debugging_enabled:
            logger.addHandler(logging.StreamHandler())
        elif not is_logging_possible:
            logger.addHandler(logging.NullHandler())
            logger.propagate = False

        # If path is set, log to file.
        if is_logging_possible:
            logger.addHandler(logging.handlers.RotatingFileHandler(
                filename=log_path,
                maxBytes=logging_config.max_size_bytes,
                backupCount=3))

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _determine_log_level(self) -> int:
        """
        Decides which messages to log based on the persisted configuration taking debug mode into account.

        Returns
        -------
        An integer defining the logging level.
        """

        if self._is_debugging_enabled:
            return logging.DEBUG

        logging_config = ConfigManager.settings.logging

        if logging_config.level is not None:
            if logging_config.level == 'critical':
                return logging.CRITICAL
            elif logging_config.level == 'debug':
                return logging.DEBUG
            elif logging_config.level == 'info':
                return logging.INFO
            elif logging_config.level == 'warning':
                return logging.WARNING

        return logging.ERROR

    def _determine_log_path(self) -> str:
        """
        Decides the exact path to the log file based on the persisted configuration, taking the override into account.

        Returns
        -------
        A string containing the path to the log file.
        """

        logging_config = ConfigManager.settings.logging

        if self._log_path_override is not None:
            return self._log_path_override
        elif logging_config.path is not None:
            return logging_config.path

        return None
