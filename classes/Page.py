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
        self.name: str = file.name # TODO: make a function that cleans up the name of the file.
        self.file: File = file
        self.tag_count: int = 0
        self.hashtags: Hashtag = set() 
        self.word_count: int = 0
        self.sentiment_tags = set() # TODO: fill sentiment tags in
        self.category = {} # TODO: analyse and fill in page category.

        self.date: datetime = crawler.get_page_date(file.name) # date in the files filename # creation date of file is not trustworthy because of git.

        # update not set variables with data from file
        self.update_hashtags()
        self.Update_word_count()

    def update_hashtags(self) -> tuple[set[Hashtag], int]:
        """
        Reads the content of the page, counts the number of unique hashtags and fills them into the set self.hashtags.

        Returns:
            hashtag_list (list): A list of unique hashtags found in the page content.
        """
        # update hashtag count
        content = reader.read_file(self.file.fullpath) 
        hashtag_list = reader.find_hashtags(content) # get list of hashtags from content
        self.tag_count = len(hashtag_list) # update tag count

        self.hashtags = reader.read_and_count_hashtags(self.file)

        return self.hashtags, self.tag_count

    def Update_word_count(self) -> int:
        """
        Reads the content of the page, counts the number of words and update self.word_count.

        Returns:
            int: The number of words in the page content.
        """
        content = reader.read_file(self.file.fullpath)
        self.word_count = reader.count_words(content)
        return self.word_count