class IndexerPolicy:
    """
    Represents a set of rules followed during the indexing process. This class knows which Collector has to be invoked
    for which types of files and also stores filters that can modify the catalogization behavior.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, collector, collectibles, filter_factory=None):
        """
        Initializes the attributes and stores the Catalogibles in a dictionary for the sake of easy lookups.

        Parameters
        ----------
        collector : Collector
            The collector to use.
        collectibles : list of Catalogible
            The list of Catalogibles to be processed by the given Collector.
        filter_factory : FilterFactory
            Provides the appropriate filters for the PathAnalyzer.
        """

        ### Validate parameters.
        if collector is None:
            raise Exception('collector cannot be None.')
        if not collectibles:
            raise Exception('collectibles cannot be None or empty.')

        ### Attributes from outside.
        self._collector = collector
        self._filter_factory = filter_factory

        ### Private attributes.
        # The filters to be used during the indexing process.
        self._filters = None
        # The name of the any tag that can match anything in the path. Includes separators.
        self._tag_any = None
        # A dictionary that stores collectibles by extensions.
        self._collectibles = self._group_collectibles_by_extensions(collectibles)

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def collector(self):
        """
        Gets the Collector for this policy.
        """
        return self._collector

    @property
    def extensions(self):
        """
        Gets extensions for this policy.
        """
        return list(self._collectibles.keys())

    @property
    def filters(self):
        """
        Gets the filters for this policy.
        """
        self._create_filters()

        return self._filters

    @property
    def tag_any(self):
        """
        Gets the name of the ANY tag.
        """
        return self._tag_any

    @tag_any.setter
    def tag_any(self, value):
        """
        Sets the name of the ANY tag.
        """
        self._tag_any = value

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def get_collectible(self, extension):
        """
        Gets the corresponding Catalogible for the given extension.

        Parameters
        ----------
        extension : str
            The extension.

        Returns
        -------
        A Collectible if there is any for the given extension, otherwise None.
        """

        if extension not in self._collectibles:
            return None

        return self._collectibles[extension]

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _create_filters(self):

        if self._filters is not None:
            return

        self._filters = []
        if self._filter_factory is not None:
            self._filters = self._filter_factory.create_filters()

    def _group_collectibles_by_extensions(self, flat_collectibles):

        collectibles = {}
        for collectible in flat_collectibles:
            for extension in collectible.extensions:
                collectibles[extension] = collectible

        return collectibles
