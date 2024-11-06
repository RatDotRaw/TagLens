import os
import sys

class File:
    """
    A class representing a file.
    """
    def __init__(self, path, name, is_dir=False):
        self.path = path
        self.name = name
        self.Is_dir = is_dir
        self.fullpath = os.path.join(path, name)

def crawl_recursive(path, hidden_files = False, max_depth=None):
    """
    crawls a directory recursively and returns a set of all files.

    Args:
        path (str): The path to the directory you want to crawl.
        hidden_files (bool): Whether to include hidden files. Defaults to False.
        max_depth (int): The maximum relative depth of the recursion. If None, it will crawl indefinitely. Defaults to None.
    
    Returns:
        set: A set containing all files found in the directory and its subdirectories.
    """
    # TODO: implement max depth functionality

    if max_depth is not None:  # Check if we should limit depth
        depth = 0

    file_set = set()
    for root, dir_names, file_names in os.walk(path):
        if max_depth is not None and depth >= max_depth:  # Stop crawling if max depth reached
            dir_names[:] = []  # Empty the list to stop further traversal
        
        depth = depth + 1 if depth is not None else depth  # Increase depth if not None
        
        for file_name in file_names:
            if file_name.startswith('.') and not hidden_files: continue
            file_set.add(File(root, file_name))
            
        for dir_name in dir_names:
            if dir_name.startswith('.') and not hidden_files: continue
            file_set.add(File(root, dir_name, Is_dir=True))
            
    
def crawl(path, hidden_files = False) -> set[File]:
    """
    Crawls a directory and returns a list of all files.

    Args:
        path (str): The path to the directory you want to crawl.
    
    Returns:
        list: A list containing all files found in the directory and its subdirectories.
    """

    file_set = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            if not hidden_files and file.startswith('.'): continue # ignore hidden files
            file_set.add(File(root, file, False))
    
    return file_set