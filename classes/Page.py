import datetime
from classes.File import File
import tools.crawler as crawler
from classes.Hashtag import Hashtag

class Page:
    """
    TODO: write description for the page class
    """
    def __init__(self, file: File):
        self.file: File = file
        self.tag_count: int = 0
        self.hashtags: Hashtag = set() # TODO: fill hashtgas in
        self.word_count: int = 0 # TODO: count words and fill word count
        self.sentiment_tags = set() # TODO: fill sentiment tags in
        self.category = {} # TODO: analyse and fill in page category.

        self.date: datetime = crawler.get_page_date(file.name) # date in the files filename # creation date of file is not trustworthy because of git.