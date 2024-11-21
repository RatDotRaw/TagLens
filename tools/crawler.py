import os
import re
import sys
import datetime
from typing import Optional

from classes.File import File

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

# function to get the created time of a file
def get_page_date(file_name: str) -> Optional[datetime]:
    """
    Returns the creation time of a file.

    Args:
        file_name (str): The filename you want to get the creation time for.
    
    Returns:
        datetime: The creation time of the file.
    """
    # check if the date is in the filename.
    # example format of filename: 2023_09_25.md
    pattern = r"(\d{4})_(\d{2})_(\d{2})\.md"
    match = re.search(pattern, file_name)
    if match:
        year, month, day = map(int, match.groups())
        return datetime.date(year, month, day)
    else: 
        # disabled because of inaccurate results. git was used on the files.
        # return datetime.fromtimestamp(os.path.getctime(path))
        return None