import os

class File:
    """
    A class representing a file.
    """
    def __init__(self, path, name, is_dir=False):
        self.path = path
        self.name = name
        self.Is_dir = is_dir
        self.fullpath = os.path.join(path, name)