import re

class PathPattern(object):
    """
    Stores a preprocessed regular expression describing a path as well as a mapping that matches the groups in that
    expression with the appropriate tags. Also stores the length of the path not counting the any tags in it.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, path_pattern_string, group_tag_mapping, length_without_any_tags):
        """
        Initializes attributes.

        Parameters
        ----------
        path_pattern_string : str
            The regular expression that each file should match as a string.
        group_tag_mapping : list of str
            Stores the tags by their indices in the pattern.
        length_without_any_tags : int
            Indicates the number of directories and files in the path pattern that are not any tags.
        """

        ### Validate parameters.
        if path_pattern_string is None:
            raise Exception('path_pattern_string cannot be None.')

        ### Attributes from outside.
        # Stores the pattern that each file forwarded to catalogizer must match as a list with the topmost directory at
        # first.
        self._path_pattern_regexp = re.compile(path_pattern_string)
        self._group_tag_mapping = group_tag_mapping
        self._length_without_any_tags = length_without_any_tags

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def group_tag_mapping(self):
        """
        Gets the collection that stores the appropriate tags for each index in the pattern.
        """
        return self._group_tag_mapping

    @property
    def length_without_any_tags(self):
        """
        Gets a number indicating the number of the nodes in the pattern, not counting nodes that can be anything.
        """
        return self._length_without_any_tags

    @property
    def path_pattern_regexp(self):
        """
        Gets the regular expression that describes the path pattern.
        """
        return self._path_pattern_regexp
