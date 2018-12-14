class ImageViewerHandler:
    """
    Interface that describes how an image viewer handler should look like.
    """

    def next(self):
        """
        Shows the next image.
        """

    def previous(self):
        """
        Shows the previous image.
        """

    def stop(self):
        """
        Exits the viewer.
        """

    def view(self, files):
        """
        Shows images from the given directory.
        """

    def zoom_in(self):
        """
        Zooms in.
        """

    def zoom_out(self):
        """
        Zooms out.
        """
