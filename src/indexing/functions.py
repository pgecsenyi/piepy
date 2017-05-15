"""
Common functions and utilities to be used by other modules.
"""

import os

def get_filename_without_extension(path):
    """
    Extracts the filename without the extension from the given path.

    Parameters
    ----------
    path : str
        The path to get the filename form.

    Returns
    -------
    The filename without the extension.
    """

    if path is None:
        return ''

    path = path.strip()
    if path == '':
        return ''

    return os.path.splitext(os.path.basename(path))[0]
