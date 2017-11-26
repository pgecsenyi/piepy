import os

from indexing.pathanalyzer import PathAnalyzer

class Indexer(object):
    """
    Traverses the given directory using the DFS algorithm. Allows registering different rules for handling different
    file types and calls the associated PathAnalyzers and Collectors indirectly for each type.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, max_depth=10):
        """
        Initializes attributes and checks the maximum depth provided.

        Parameters
        ----------
        max_depth : int
            The maximum depth to look in.
        """

        ### Validate parameters.
        if max_depth < 1:
            raise Exception('max_depth must be greater than or equal to 1.')

        ### Attributes from outside.
        self._max_depth = max_depth

        ### Private attributes.
        # A collection of analyzers which handle different file types.
        self._analyzers = []
        # This dictionary stores which analyzer is associated to which file extension.
        self._analyzers_by_extensions = {}
        # The depth we are currently in.
        self._current_depth = 0
        # The list of directories to index.
        self._directories = []

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def add_directory(self, directory):
        """
        Registers a new directory to index.

        Parameters
        ----------
        directory : str
            The directory to be indexed.
        """

        self._directories.append(directory)

    def add_policy(self, policy):
        """
        Registers a new policy.

        Parameters
        ----------
        policy : IndexerPolicy
            The policy to register.
        """

        analyzer = PathAnalyzer(policy)
        self._analyzers.append(analyzer)

        for extension in policy.extensions:
            if extension not in self._analyzers_by_extensions.keys():
                self._analyzers_by_extensions[extension] = analyzer

    def index(self):
        """
        Initializes filters, initiates indexing and after the indexing process has finished, cleans filters.
        """

        for analyzer in self._analyzers:
            analyzer.init_filters()

        for directory in self._directories:
            if os.path.exists(directory):
                self._scan_directory(directory)

        for analyzer in self._analyzers:
            analyzer.clean_filters()

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _analyze_file(self, current_path):

        current_path_without_extension, current_extension = os.path.splitext(current_path)
        if current_extension in self._analyzers_by_extensions:
            analyzer = self._analyzers_by_extensions[current_extension]
            if analyzer != None:
                analyzer.analyze(current_path_without_extension, current_extension)

    def _enter(self, directory):
        """
        Indicates for the analyzers that we entered into the given directory.

        Parameters
        ----------
        directory : str
            The directory we entered.
        """

        for analyzer in self._analyzers:
            analyzer.enter(directory)

        self._current_depth = self._current_depth + 1

    def _leave(self):
        """
        Indicates for the analyzers that we are leaving the last directory.
        """

        for analyzer in self._analyzers:
            analyzer.leave()

        self._current_depth = self._current_depth - 1


    def _scan_directory(self, path):
        """
        Does the real indexing. Iterates through the directory using DFS, and invokes the registered analyzers to
        analyze and store the data.

        Parameters
        ----------
        path : str
            The path to enumerate.
        """

        for current_file in os.listdir(path):

            current_path = os.path.join(path, current_file)

            if self._current_depth >= self._max_depth:
                return

            if os.path.isdir(current_path):
                self._enter(current_file)
                self._scan_directory(current_path)
                self._leave()
            else:
                self._analyze_file(current_path)
