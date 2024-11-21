import os

class File:
    """
    A class representing a file.

    Attributes:
        path (str): The directory path of the file.
        name (str): The name of the file.
        Is_dir (bool): A flag indicating whether the file is a directory or not.
        fullpath (str): The full path of the file.
    """
    def __init__(self, path, name, is_dir=False):
        self.path = path
        self.name = name
        self.Is_dir = is_dir
        self.fullpath = os.path.join(path, name)