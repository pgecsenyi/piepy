from indexing.strrange import StrRange

class PathPatternPreprocessor:
    """
    Normalizes the path, escapes special characters in it, checks whether it is stable and calculates it's length.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):
        """
        Initializes the attributes.
        """

        ### Private attributes.
        # The full shape of the ANY tag.
        self._any_tag_complete = None
        # The length of the path (the number of nodes in it) without the ANY tags.
        self._length_without_any_tags = 0
        # The path pattern string.
        self._path_pattern_string = None
        # The tag configuration.
        self._tag_config = None

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def length_without_any_tags(self):
        """
        Gets the length of the path pattern excluding the ANY tags.
        """
        return self._length_without_any_tags

    @property
    def path_pattern_string(self):
        """
        Gets the path pattern string.
        """
        return self._path_pattern_string

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def process(self, tag_config, path_pattern_string):
        """
        Preprocesses the given path.

        Parameters
        ----------
        tag_config : TagConfig
            The tag configuration.
        path_pattern_string : str
            The path pattern as a string.
        """

        if tag_config is None:
            raise Exception('tag_config cannot be None.')
        if path_pattern_string is None or path_pattern_string.strip() == '':
            raise Exception('path_pattern_string cannot be None or empty.')

        self._set_attributes(tag_config, path_pattern_string)
        self._normalize_path()
        self._preprocess_path_pattern()

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _build_any_tag_complete(self):

        self._any_tag_complete = None
        if self._tag_config.tag_any is not None:
            self._any_tag_complete = self._tag_config.start + self._tag_config.tag_any[0] + self._tag_config.end

    def _check_consecutive_tags(self):

        is_after_tag = False

        for char in self._path_pattern_string:

            if is_after_tag and char == self._tag_config.start:
                return True

            is_after_tag = char == self._tag_config.end

        return False

    def _check_if_path_is_stable(self):
        """
        A path is stable
          * if it does not contain ANY tags
          * OR it has a fix point (a directory with a constant name, without ANY tags).
        Also calculates the length without ANY tags.

        Returns
        -------
        A boolean value indicating whether the path is stable or not.
        """

        contains_fix_point = False
        path_pattern_as_list = self._path_pattern_string.split('/')

        # Iterate through every node in the path pattern.
        for path_pattern in path_pattern_as_list:

            # Get the tag from the current item.
            current_item = path_pattern
            is_fixpoint = True
            is_in_tag = False
            tag_range = StrRange()

            # pylint: disable=consider-using-enumerate
            for char_index in range(0, len(current_item)):
                char = current_item[char_index]
                if is_in_tag and char == self._tag_config.end:
                    is_fixpoint = False
                    tag_range.end = char_index
                    break
                elif char == self._tag_config.start:
                    is_fixpoint = False
                    tag_range.start = char_index
                    is_in_tag = True

            # Check if we have a fix point so far (have one already or the current node is fix).
            contains_fix_point = contains_fix_point or is_fixpoint

            # Update the length attribute (calculate length without the ANY tags).
            if tag_range.length != (len(current_item) - 1) or current_item != self._any_tag_complete:
                self._length_without_any_tags = self._length_without_any_tags + 1

        return contains_fix_point or self._length_without_any_tags == len(path_pattern_as_list)

    def _escape_special_characters(self, unescaped_string):
        """
        Escapes those special characters in a string which would cause trouble in a regular expression.

        Parameters
        ----------
        unescaped_string : str
            The string to escape.

        Returns
        -------
        The escaped string.
        """

        escaped_string = ''
        special_regexp_characters = ['.', '^', '$', '*', '+', '?', '(', ')', '[', ']', '{', '}', '\\', '|']

        for char in unescaped_string:
            if char in special_regexp_characters:
                escaped_string = escaped_string + '\\' + char
            else:
                escaped_string = escaped_string + char

        return escaped_string

    def _normalize_path(self):

        self._path_pattern_string = self._path_pattern_string.replace('\\', '/')

    def _preprocess_path_pattern(self):
        """
        Checks if the path pattern contains no ambiguous parts and escapes the special regular expression characters in
        it.

        Returns
        -------
        The escaped string.
        """

        # In case the path does not have a fix point, it must not contain ANY tags.
        if not self._check_if_path_is_stable():
            raise Exception(
                'In case the path contains at least one ANY tag, then it also has to have at least one fix point (a '
                'directory with a well-defined constant text).')

        # Check that there are no two tags next to each other anywhere in the path.
        if self._check_consecutive_tags():
            raise Exception('There cannot be two tags directly next to each other in the path.')

        # Escape the special characters.
        self._path_pattern_string = self._escape_special_characters(self._path_pattern_string)

    def _set_attributes(self, tag_config, path_pattern_string):

        self._length_without_any_tags = 0
        self._path_pattern_string = path_pattern_string
        self._tag_config = tag_config

        self._build_any_tag_complete()
