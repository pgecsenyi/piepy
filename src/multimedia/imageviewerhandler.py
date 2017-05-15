class ImageViewerHandler(object):
    """
    Interface that describes how an image viewer handler should look like.
    """

    def next(self):
        """
        Shows the next image.
        """
        pass

    def previous(self):
        """
        Shows the previous image.
        """
        pass

    def stop(self):
        """
        Exits the viewer.
        """
        pass

    def view(self, files):
        """
        Shows images from the given directory.
        """
        pass

    def zoom_in(self):
        """
        Zooms in.
        """
        pass

    def zoom_out(self):
        """
        Zooms out.
        """
        pass
