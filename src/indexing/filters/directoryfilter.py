import re

from indexing.filters.pathfilter import PathFilter

class DirectoryFilter(PathFilter):
    """
    Ignores a path if the last directory in it matches the given pattern.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, pattern_string):

        ### Validate parameters.
        if pattern_string is None:
            raise Exception('pattern_string cannot be None.')

        ### Private attributes.
        # Indicates whether the paths in the current depth are just revisions so we do not need to check it again and
        # again.
        self._is_revision = False
        # Indicates whether the current depth was checked against being a revision.
        self._is_revision_checked = False
        # The pattern of tha paths which this filter ignores.
        self._pattern = re.compile(pattern_string)

    ####################################################################################################################
    # Filter implementation.
    ####################################################################################################################

    def apply_filter(self, path):

        if self._is_revision_checked:
            return self._is_revision

        last_directory_name = self._get_last_directory_name(path)

        match = self._pattern.search(last_directory_name)
        if match is None:
            self._is_revision = False
        else:
            self._is_revision = True

        self._is_revision_checked = True

        return self._is_revision

    def clean_filter(self):

        pass

    def init_filter(self):

        pass

    def leave_scope(self):

        self._is_revision_checked = False

    ####################################################################################################################
    # Auxiliary methods.
    ####################################################################################################################

    def _get_last_directory_name(self, path):

        end_index = -1
        start_index = -1

        for i in range(len(path) - 1, 0, -1):
            if path[i] == '/':
                if end_index == -1:
                    end_index = i
                else:
                    start_index = i
                    break

        if end_index == -1 or start_index == -1:
            return path

        return path[(start_index + 1) : end_index]
