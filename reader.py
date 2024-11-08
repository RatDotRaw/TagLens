import re
import logging
from typing import List, Set
from crawler import File

class Hashtag:
    """A class representing a hashtag.

    Attributes:
        hashtag (str): The text of the hashtag.
        count (int): The number of times the hashtag appears in the text.   
        source (Set[File]): A set of files where the hashtag appears.
    """
    def __init__(self, text, source):
        self.name = text
        self.count = 1
        self.sources: Set[File] = set()

        self.add_source(source)
    
    def __hash__(self):
        return hash(self.name)  # Use name for hashing

    def add_source(self, source):
        self.sources.add(source)

# func to read and return the content of a text file
def read_file(filename) -> str:
    """Reads a text file and returns its content.
    
    Args:
        filename (str): The name of the file to read.
    
    Returns:
        str: The content of the file.
    """
    # try to open and read the file
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        logging.error("File not found.")
        return ""
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        return ""

# func to find all regex matches in a text
def find_hashtags(text) -> list:
    """Finds all hashtags in a given text.

    Args:
        text (str): The text to search for hashtags.
    
    Returns:
        set: A set of unique hashtags found in the text.
    """
    re_pattern = r"#([^\[.,!?;:\s#]+)|#\[\[([^\]]+)\]\]"
    return [match[0] if match[0] else match[1] for match in re.findall(re_pattern, text)]

def read_and_count_hashtags(file: File) -> Set[Hashtag]:
    """
    Reads a file and counts the occurrences of each hashtag in it.

    Args:
        file (File): The file to read and count hashtags in.

    Returns:
        set: A set of unique hashtags found in the file.
    """
    hashtags: Set[Hashtag] = set()
    hastag_names = set()

    content = read_file(file.fullpath)
    for hashtag in find_hashtags(content):
        # check if the match already exists in the set
        if not any(h.name.strip().lower() == hashtag.strip().lower() for h in hashtags):
            hashtags.add(Hashtag(hashtag, file))
    return hashtags

    # get unique hashtags and create a Hashtag object foreach one linking to the file where it was found

def read_all_and_count_hashtags(files: List[File]) -> Set[Hashtag]:
    """
    Reads all files in a list and counts the occurrences of each hashtag.
    
    Args:
        files (List[File]): The list of files to read and count hashtags in.
    
    Returns:
        set: A set of unique hashtags found in all files.
    """
    all_hashtags: Set[Hashtag] = []
    for file in files:
        all_hashtags.extend(read_and_count_hashtags(file))

    all_unique_hashtags: set[Hashtag] = set()
    for hashtag in all_hashtags:
        if not any(h.name == hashtag.name for h in all_unique_hashtags):
            all_unique_hashtags.add(hashtag)
        else:
            # find and increase count and sources of the duplicate hashtag
            for h in all_unique_hashtags:
                if h.name == hashtag.name:
                    h.count += hashtag.count
                    h.sources.update(hashtag.sources)
    return all_unique_hashtags

def count_words(content: str) -> int:
    """
    Reads and counts the total amount of words in the given content.

    Args:
        content (str): The text to count words in.

    Returns:
        int: The count of words found in the text.
    """
    words = re.findall(r"\b\w+\b", content)  # Find all words with pattern
    return len(words)
