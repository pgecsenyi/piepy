from indexing.pathpattern import PathPattern
from indexing.pathpatternpreprocessor import PathPatternPreprocessor

class PathPatternAnalyzer:
    """
    Receives a path containing tags as a string and builds a regular expression from it (to be more precise, it builds a
    PathPattern object).
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):
        """
        Initializes the attributes.
        """

        ### Private attributes.
        # A list that maps the groups in the pattern to the corresponding tags.
        self._group_tag_mapping = []
        # The path pattern string.
        self._path_pattern_string = None
        # The regular expression built from the input string.
        self._path_pattern_regexp = ''
        # The tag configuration.
        self._tag_config = None

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def parse(self, tag_config, path_pattern_string):
        """
        Parses the given string.

        Parameters
        ----------
        tag_config : TagConfig
            The tag configuration.
        path_pattern_string : str
            The path pattern as a string.

        Returns
        -------
        The PathPattern object.
        """

        # Validate arguments.
        if tag_config is None:
            raise Exception('tag_config cannot be None.')
        if path_pattern_string is None or path_pattern_string.strip() == '':
            raise Exception('path_pattern_string cannot be None or empty.')

        # Re-initialize attributes.
        self._set_attributes(tag_config, path_pattern_string)

        # Preprocess the pattern.
        preprocessor = PathPatternPreprocessor()
        preprocessor.process(tag_config, path_pattern_string)
        self._path_pattern_string = preprocessor.path_pattern_string

        # Process the pattern.
        self._process_tags()

        return PathPattern(self._path_pattern_regexp, self._group_tag_mapping, preprocessor.length_without_any_tags)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _collect_groups(self):
        """
        Prepares the regular expression string from the path pattern string. (Does not create the final regular
        expression, only places internal tags to be substituted later using the format string function. In the
        same times creates the group-tag mapping which will be used for this purpose.)

        Returns
        -------
        The list of characters following ANY tags.
        """

        after_any_tags = []
        current_group_index = 0
        current_tag = ''
        is_after_any_tag = False
        is_in_tag = False

        for char in self._path_pattern_string:

            # Remember the characters after ANY tags, they will be needed when building the regular expression.
            if is_after_any_tag:
                after_any_tags.append(char)
                is_after_any_tag = False
            # Update the group-tag mapping and check if the tag is an ANY tag.
            elif is_in_tag:
                if char == self._tag_config.end:
                    self._verify_tag(current_tag)
                    if (self._tag_config.tag_any is not None) and (current_tag == self._tag_config.tag_any[0]):
                        is_after_any_tag = True
                    self._path_pattern_regexp = self._path_pattern_regexp + '{0[' + str(current_group_index) + ']}'
                    self._group_tag_mapping.append(current_tag)
                    is_in_tag = False
                    current_tag = ''
                    current_group_index = current_group_index + 1
                else:
                    current_tag = current_tag + char
            # Store the current character as a part of the regular expression skeleton or as a part of a tag.
            else:
                if char == self._tag_config.start:
                    is_in_tag = True
                else:
                    self._path_pattern_regexp = self._path_pattern_regexp + char

        return after_any_tags

    def _process_tags(self):
        """
        Finalizes the regular expression by substituting the group indices with the appropriate groups.
        """

        after_any_tag_index = 0
        after_any_tags = self._collect_groups()
        special_tag_patterns = []

        # Iterate through the group-tag mapping and substitute ANY tags.
        for tag in self._group_tag_mapping:
            if (self._tag_config.tag_any is not None) and (tag == self._tag_config.tag_any[0]):
                char_after_any_tag = ''
                if after_any_tag_index < len(after_any_tags):
                    char_after_any_tag = after_any_tags[after_any_tag_index]
                special_tag_patterns \
                    .append('({}{}|)'.format(self._tag_config.tag_any[1], char_after_any_tag))
                after_any_tag_index = after_any_tag_index + 1
            else:
                special_tag_patterns.append(self._tag_config.tag_patterns[tag])

        # Substitute the more specific patterns and finalize the expression.
        self._path_pattern_regexp = self._path_pattern_regexp.format(special_tag_patterns)
        self._path_pattern_regexp = self._path_pattern_regexp + '$'

    def _set_attributes(self, tag_config, path_pattern_string):

        self._group_tag_mapping = []
        self._path_pattern_string = path_pattern_string
        self._path_pattern_regexp = ''
        self._tag_config = tag_config

    def _verify_tag(self, tag):
        """
        Checks whether the given tag is allowed in the pattern and throws if not.

        Parameters
        ----------
        tag : str
            The tag to verify.
        """

        if (self._tag_config.tag_any is not None) and (tag == self._tag_config.tag_any[0]):
            return
        if tag not in self._tag_config.tag_patterns.keys():
            raise Exception('The path contains an invalid tag: ' + tag + '.')
