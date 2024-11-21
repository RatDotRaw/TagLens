import datetime
from classes.File import File
import tools.crawler as crawler
import tools.reader as reader
from classes.Hashtag import Hashtag
import tools.analysis as analysis

class SentimentTag:
    """
    A class to represent the sentiment analysis result for a page.

    Attributes:
        text: The text that was analyzed.
        sentiment: A string indicating the sentiment of the text ('positive', 'negative', or 'neutral').
        confidence: A float representing the confidence level of the sentiment analysis (0-1).

    Methods:
        TODO: (add methods here as they are implemented)
    """
    def __init__(self, text: str, sentiment: str, confidence: float):
        self.text = text
        self.sentiment = sentiment
        self.confidence = confidence


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
        self.sentiment_tags: list[dict] = None # TODO: fill sentiment tags in
        self.category = {} # TODO: analyse and fill in page category.

        self.journal_entry: bool = False 
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
    
    # DO NOT RUN ON INIT OR IT WILL BE TOO SLOW. ONLY RUN WHEN REQUIRED.
    def Update_sentiment_tags(self, threshold: float = 0.2):
        """
        Analyzes the sentiment of the page content and updates self.sentiment_tags
        Do not run on init or it will be too slow. Only run when required.

        Args:
            threshold (float): The minimum confidence level required for a sentiment tag to be added to the set. Defaults to 0.1.

        Returns:
            None
        """
        content = reader.read_file(self.file.fullpath)
        tag_scores = analysis.text_to_emotions(content)

        filtered = []
        # remove tags with confidence less than threshold
        for tag in tag_scores:
            if tag["score"] > threshold:
                filtered.append(tag)
        self.sentiment_tags = filtered