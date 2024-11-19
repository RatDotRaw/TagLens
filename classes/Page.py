import datetime
from classes.File import File
import tools.crawler as crawler
import tools.reader as reader
from classes.Hashtag import Hashtag

class Page:
    """
    A container class to hold information about a Logseq page.

    Attributes:
        file: The original File object that this Page is based on.
        tag_count: The total number of tags associated with this page.
        hashtags: A set of Hashtag objects representing the unique tags used on this page.
        word_count: The total number of words in the text of this page.
        sentiment_tags: A set of SentimentTag objects indicating the sentiment analysis result for this page.
        category: A dictionary containing the categorization result for this page.
        date: The date when the file was created, inferred from its filename.

    Methods:
        TODO: (add methods here as they are implemented)
    """
    def __init__(self, file: File):
        self.file: File = file
        self.tag_count: int = 0
        self.hashtags: Hashtag = set() # TODO: fill hashtgas in
        self.word_count: int = 0 # TODO: count words and fill word count
        self.sentiment_tags = set() # TODO: fill sentiment tags in
        self.category = {} # TODO: analyse and fill in page category.

