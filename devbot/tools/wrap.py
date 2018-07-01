"""
    A wrapper for files so we can send files easily
"""

import os.path


class FileWrapper:
    """ A wrapper for files so we can send files easily """
    def __init__(self, filename):
        if os.path.exists(filename):
            self.file = filename
        else:
            raise FileNotFoundError(f"No file found by following {filename}")

    @property
    def name(self):
        """ Return the file's name. """
        return self.file
