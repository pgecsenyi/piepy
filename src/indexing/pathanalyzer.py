from indexing.nodes import CategorizedNode, UncategorizedNode

class PathAnalyzer(object):
    """
    Analyzes paths. Matches the given pattern on the given files, collecting the ones that match the pattern and the
    ones that do not separately. Forwards the collected data to the Collector in batches when all the necessary
    information become available.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, policy):
        """
        Initializes attributes.

        Parameters
        ----------
        policy : IndexerPolicy
            The policy to follow.
        """

        ### Validate parameters.
        if policy is None:
            raise Exception('policy cannot be None.')

        ### Attributes from outside.
        self._policy = policy

        ### Private attributes.
        # The categorized file data to be committed when fix point is reached.
        self._categorized_nodes = []
        # The current depth of directory hierarchy we are in.
        self._current_depth = 0
        # Inflection points indicate the directory level at which collected data should be forwarded to the Collector.
        # It could also be colled "commit point".
        self._inflection_point = -1
        # Stores the last node (directory) we iterated through as an uncategorized node.
        self._last_node_as_uncategorized = None
        # The format of the any tag that can match anything in the path. Includes separators.
        self._tag_any = None
        # The collection of files which do not match the predefined pattern and should be commited as uncategorized
        # files at the end.
        self._uncategorized_nodes = []

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def analyze(self, path, extension):
        """
        Analyzes the given path and checks if it conforms to the pre-defined custom path and builds an appropriate meta
        data container object in that case.

        Parameters
        ----------
        path : str
            The path to analyze.
        extensions : str
            The extension part of the path.
        """

        # No path to analyze. Nothing to do here.
        if path is None or not path:
            return

        # No collectible for this extension. Nothing to do here.
        collectible = self._policy.get_collectible(extension)
        if collectible is None:
            return

        # Check if path should be filtered out.
        full_path = path + extension
        for path_filter in self._policy.filters:
            if path_filter.apply_filter(full_path):
                return

        # Decide whether this path is categorized correctly or not and append the file to the appropriate list.
        node = self._try_match_pattern(collectible.path_pattern, path, extension)

        if node is None:
            uncategorized_node = UncategorizedNode(full_path, self._last_node_as_uncategorized)
            uncategorized_node.token = collectible.token
            self._uncategorized_nodes.append(uncategorized_node)
        else:
            node.token = collectible.token
            self._categorized_nodes.append(node)

    def clean_filters(self):
        """
        Cleans the registered filters.
        """

        for path_filter in self._policy.filters:
            path_filter.clean_filter()

    def enter(self, directory):
        """
        Notifies filters of scope change, stores the directory we entered as an UncategorizedNode and maintains a
        counter of the current depth.

        Parameters
        ----------
        directory : str
            The name of the directory we just entered.
        """

        for path_filter in self._policy.filters:
            path_filter.leave_scope()

        self._last_node_as_uncategorized = UncategorizedNode(directory, self._last_node_as_uncategorized)
        self._current_depth = self._current_depth + 1

    def init_filters(self):
        """
        Initializes the registered filters.
        """

        for path_filter in self._policy.filters:
            path_filter.init_filter()

    def leave(self):
        """
        Notifies filters of scope change, jumps up in the UncategorizedNode tree, maintains current depth counter and
        calls the Collector if needed.
        """

        for path_filter in self._policy.filters:
            path_filter.leave_scope()

        if self._last_node_as_uncategorized != None:
            self._last_node_as_uncategorized = self._last_node_as_uncategorized.parent

        self._current_depth = self._current_depth - 1

        if self._current_depth <= 0 and self._uncategorized_nodes:
            self._process_uncategorized_batch()

        if self._current_depth <= self._inflection_point:
            if self._categorized_nodes:
                self._process_batch()
            self._inflection_point = -1

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _process_batch(self):
        """
        Calls the Collector to process the current batch of categorized files.
        """

        self._policy.collector.collect_categorized(self._categorized_nodes)
        self._categorized_nodes = []

    def _process_uncategorized_batch(self):
        """
        Calls the Collector to process the current batch of uncategorized files.
        """

        self._policy.collector.collect_uncategorized(self._uncategorized_nodes)
        self._uncategorized_nodes = []

    def _try_match_pattern(self, path_pattern, path, extension):
        """
        Tries to match the given pattern to the given path and decides whether the given path is categorized or not.

        Parameters
        ----------
        path_pattern : PathPattern
            The pattern the path should match.
        path : str
            The path to analyze.
        extensions : str
            The extension part of the path.

        Returns
        -------
        The node containing the meta data or None if the path does not match the pattern.
        """

        depth = 0
        matches = path_pattern.path_pattern_regexp.search(path)
        node = None

        if matches != None:

            depth = path_pattern.length_without_any_tags
            node = CategorizedNode(path + extension)
            i = 0

            for match in matches.groups():
                if match != None and match != '':
                    if path_pattern.group_tag_mapping[i] == self._policy.tag_any:
                        depth = depth + 1
                    else:
                        node.meta[path_pattern.group_tag_mapping[i]] = match
                i = i + 1

        if self._inflection_point == -1:
            self._inflection_point = self._current_depth - depth + 1
        else:
            self._inflection_point = min(self._inflection_point, path_pattern.length_without_any_tags)

        return node
