from classes.File import File
import tools.crawler as crawler

from datetime import datetime
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

        self.first_appearance_date: datetime = None
        self.last_appearance_date: datetime = None

        self.add_source(source)

    def __hash__(self):
        return hash(self.name)  # Use name for hashing

    # TODO: Bug: The first and last dates are not correct in my testing. problem lies likely somewhere else... (if i only wrote tests...)
    def add_source(self, source: File):
        date = crawler.get_page_date(source.name)

        # Check if the source already exists
        for s in self.sources:
            if s.name == source.name:
                return  # Source already exists

        if date:
            # Update first_appearance_date
            if self.first_appearance_date is None or date < self.first_appearance_date:
                self.first_appearance_date = date

            # Update last_appearance_date
            if self.last_appearance_date is None or date > self.last_appearance_date:
                self.last_appearance_date = date

        self.sources.add(source)