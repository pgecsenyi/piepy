class PathAnalyzerStore(object):
    """
    Maps extensions to analyzers. To be used for storing the analyzers that should be used for specific extensions in a
    directory.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        # This dictionary stores the corresponding analyzer for each extension.
        self._analyzers_by_extensions = {}

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def add_analyzer(self, extensions, analyzer):

        for extension in extensions:

            if extension in self._analyzers_by_extensions:
                raise Exception(
                    F'Invalid configuration, an analyzer is already registered for the extension "{extension}". Do not '
                    'register multiple rules for the same extensions in a directory.')

            self._analyzers_by_extensions[extension] = analyzer

    def find_analyzer(self, extension):

        return self._analyzers_by_extensions.get(extension, None)
