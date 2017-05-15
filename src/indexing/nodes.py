class Node(object):
    """
    Stores the path of a file system entry. Also stores a token for it, which for example can be an identifier of it's
    type.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, path):
        """
        Stores the path of this Node.

        Parameters
        ----------
        path : str
            The path of the file this Node represents.
        """

        ### Attributes from outside.
        self._path = path

        # Private attributes.
        self._token = None

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def path(self):
        """
        Gets the path of the file this Node represents.
        """
        return self._path

    @property
    def token(self):
        """
        Gets the optional token provided with this Node.
        """
        return self._token

    @token.setter
    def token(self, value):
        """
        Sets the optional token for this Node.
        """
        self._token = value

class CategorizedNode(Node):
    """
    Stores information (path and metadata) about a categorized file. Used by the Collector.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, path):
        """
        Calls the base class constructor and initializes the dictionary for the meta data.

        Parameters
        ----------
        path : str
            The path of this node.
        """

        ### Call base class constructor.
        super(CategorizedNode, self).__init__(path)

        ### Private attributes.
        # Meta data as string => string pairs, where the keys should be tags.
        self._meta = {}

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def meta(self):
        """
        Gets the dictionary containing this Node's meta data.
        """
        return self._meta

class UncategorizedNode(Node):
    """
    Stores information (path and parent) about an uncategorized file. Used by the Collector.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, path, parent=None):
        """
        Calls the base class constructor and stores the parent of this UncategorizedNode instance.

        Parameters
        ----------
        path : str
            The path of this node.
        parent : UncategorizedNode
            The parent of this node.
        """

        ### Call base class constructor.
        super(UncategorizedNode, self).__init__(path)

        ### Attributes from outside.
        self._parent = parent

        ### Private attributes.
        # The ID of this path in the database. This field is used by the Collector.
        self._id_in_database = -1

    ####################################################################################################################
    # Properties.
    ####################################################################################################################

    @property
    def id_in_database(self):
        """
        Gets the database entry ID of this Node.
        """
        return self._id_in_database

    @id_in_database.setter
    def id_in_database(self, value):
        """
        Sets the database entry ID of this Node.
        """
        self._id_in_database = value

    @property
    def parent(self):
        """
        Gets the parent of this Node.
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        """
        Sets the parent of this Node.
        """
        self._parent = value
