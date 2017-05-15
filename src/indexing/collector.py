class Collector(object):
    """
    Interface that describes file processors: the path analyzer will forward each analyzed file (to be more precise,
    the analyzed files in a batch) to a Collector implementation which supposed to store structured data, execute
    database operations and so on.
    """

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def collect_categorized(self, categorized_nodes):
        """
        This method is called for files that match the pattern provided.

        Parameters
        ----------
        categorized_nodes : list of CategorizedNode
            The list of the nodes to collect.
        """
        pass

    def collect_uncategorized(self, uncategorized_nodes):
        """
        This method is called for files that do not match the pattern provided.

        Parameters
        ----------
        uncategorized_nodes : list of UncategorizedNode
            The list of the nodes to collect.
        """
        pass
