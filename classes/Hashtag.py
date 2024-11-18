from classes.File import File


import datetime
from typing import Set


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

        self.first_appearance_date: datetime.datetime = None
        self.last_appearance_date: datetime.datetime = None

        self.add_source(source)

    def __hash__(self):
        return hash(self.name)  # Use name for hashing

    def add_source(self, source):
        self.sources.add(source)