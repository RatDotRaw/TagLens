from classes.File import File
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