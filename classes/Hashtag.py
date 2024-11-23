from classes.File import File
import tools.crawler as crawler

import datetime
from typing import Set


class Hashtag:
    """A class representing a hashtag.

    Attributes:
        hashtag (str): The text of the hashtag.
        count (int): The number of times the hashtag appears in the text.   
        source (Set[File]): A set of files where the hashtag appears.
        first_appearance_date (datetime.datetime): The date and time when the first appearance of the hashtag was found.
        last_appearance_date (datetime.datetime): The date and time when the last appearance of the hashtag was found.
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

    def add_source(self, source: File):
        date = crawler.get_page_date(source.name)
        if date:
            # check if the date is newer than the current first appearance or older than the last appearance
            if self.first_appearance_date is None or date < self.first_appearance_date:
                self.first_appearance_date = date

            if self.last_appearance_date is None or date > self.last_appearance_date:
                self.last_appearance_date = date

        self.sources.add(source)