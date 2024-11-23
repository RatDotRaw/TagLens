import tools.crawler as crawler
import tools.reader as reader
from classes.Page import Page
import logging

logseq_base_path = "/home/stafd/Documents/git/logseq"

logging.getLogger().setLevel(logging.INFO)

def read_hashtags():
    # gather list of all files to be scanned
    journal_files = crawler.crawl(f"{logseq_base_path}/journals")
    pages_files = crawler.crawl(f"{logseq_base_path}/pages")
    # get all unique hashtags, their count, and source file
    hashtag_set = reader.read_all_and_count_hashtags(journal_files)
    hashtag_set = hashtag_set.union(reader.read_all_and_count_hashtags(pages_files))
    
    return hashtag_set

def read_pages():
    # gather list of all files to be scanned
    journal_files = crawler.crawl(f"{logseq_base_path}/journals")
    pages_files = crawler.crawl(f"{logseq_base_path}/pages")

    logging.info("Reading pages")
    pages_set: set[Page] = set()
    for file in journal_files:
        page = Page(file)
        
        # set Page.journal_entry to true for all journal entries
        page.journal_entry = True

        pages_set.add(page)
    logging.info(f"Total pages loaded: ${len(pages_set)}")
    
    # Set sentiments for only journal entries
    logging.info("Updating sentiment tags for journal entries")
    for page in pages_set:
        print(f"page: {page.name}, journal entry: {page.journal_entry}")
        if page.journal_entry:
            logging.info(f"Updating sentiment tags for {page.name}")
            page.Update_sentiment_tags(threshold=0.3)

def main():
    hashtag_set = read_hashtags()
    page_set = read_pages()
    

if __name__ == "__main__":
    main()