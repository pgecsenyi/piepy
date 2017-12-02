from indexing.pathpattern import PathPattern

class PathPatternAnalyzer(object):
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
        # The length of the path (the number of nodes in it) without the ANY tags.
        self._length_without_any_tags = 0
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
        self._group_tag_mapping = []
        self._length_without_any_tags = 0
        self._path_pattern_string = path_pattern_string
        self._path_pattern_regexp = ''
        self._tag_config = tag_config

        # Process the pattern.
        self._preprocess_path_pattern()
        self._process_tags()

        return PathPattern(self._path_pattern_regexp, self._group_tag_mapping, self._length_without_any_tags)

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _check_if_stable_path(self):
        """
        Checks if the path is stable:
          * it has a fix point (a directory with a constant name, without ANY tags)
          * OR it does not contain ANY tags.
        Also calculates the length without ANY tags.

        Returns
        -------
        A boolean value indicating whether the path is stable or not.
        """

        complete_any_tag = None
        if self._tag_config.tag_any != None:
            complete_any_tag = self._tag_config.start + self._tag_config.tag_any[0] + self._tag_config.end
        contains_fix_point = False
        path_pattern_as_list = self._path_pattern_string.split('/')

        # Iterate through every node in the path pattern.
        for i in range(0, len(path_pattern_as_list)):

            # Get the tag from the current item.
            is_fixpoint = True
            is_in_tag = False
            tag_start = 0
            tag_end = 0

            for j in range(0, len(path_pattern_as_list[i])):
                char = path_pattern_as_list[i][j]
                if is_in_tag and char == self._tag_config.end:
                    is_fixpoint = False
                    tag_end = j
                    break
                elif char == self._tag_config.start:
                    is_fixpoint = False
                    tag_start = j
                    is_in_tag = True

            # Check if we have a fix point so far (have one already or the current node is fix).
            contains_fix_point = contains_fix_point or is_fixpoint

            # Update the length attribute (calculate length without the ANY tags).
            if tag_start != 0 \
                or tag_end != (len(path_pattern_as_list[i]) - 1) \
                or path_pattern_as_list[i] != complete_any_tag:
                self._length_without_any_tags = self._length_without_any_tags + 1

        return contains_fix_point or self._length_without_any_tags == len(path_pattern_as_list)

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
                    if (self._tag_config.tag_any != None) and (current_tag == self._tag_config.tag_any[0]):
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

    def _preprocess_path_pattern(self):
        """
        Checks if the path pattern string is stable and there are no ambiguous parts in it. Finally escapes the special
        regular expression characters in it.

        Parameters
        ----------
        unescaped_string : str
            The string to escape.

        Returns
        -------
        The escaped string.
        """

        # Normalize path.
        self._path_pattern_string = self._path_pattern_string.replace('\\', '/')

        # In case the path does not have a fix point, it must not contain ANY tags.
        if not self._check_if_stable_path():
            raise Exception(
                'In case the path contains at least one ANY tag, then it also has to have at least one fix point (a '
                'directory with a well-defined constant text).')

        # Check that there are no two tags next to each other anywhere in the path.
        is_after_tag = False
        for char in self._path_pattern_string:
            if is_after_tag and char == self._tag_config.start:
                raise Exception('There cannot be two tags directly next to each other in the path.')
            elif char == self._tag_config.end:
                is_after_tag = True
            else:
                is_after_tag = False

        # Escape the special characters.
        self._path_pattern_string = self._escape_special_characters(self._path_pattern_string)

    def _process_tags(self):
        """
        Finalizes the regular expression by substituting the group indices with the appropriate groups.
        """

        after_any_tag_index = 0
        after_any_tags = self._collect_groups()
        special_tag_patterns = []

        # Iterate through the group-tag mapping and substitute ANY tags.
        for tag in self._group_tag_mapping:
            if (self._tag_config.tag_any != None) and (tag == self._tag_config.tag_any[0]):
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

    def _verify_tag(self, tag):
        """
        Checks whether the given tag is allowed in the pattern and throws if not.

        Parameters
        ----------
        tag : str
            The tag to verify.
        """

        if (self._tag_config.tag_any != None) and (tag == self._tag_config.tag_any[0]):
            return
        if tag not in self._tag_config.tag_patterns.keys():
            raise Exception('The path contains an invalid tag: ' + tag + '.')
