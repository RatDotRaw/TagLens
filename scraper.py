from dotenv import load_dotenv
load_dotenv()

import os
import tools.crawler as crawler
import tools.reader as reader
from classes.Page import Page
import logging
from database.DatabaseFactory import DatabaseFactory

logseq_base_path = os.getenv("LOGSEQ_BASE_PATH")

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

    for file in pages_files:
        page = Page(file)
        pages_set.add(page)

    logging.info(f"Total pages loaded: ${len(pages_set)}")
    
    # Set sentiments for only journal entries
    logging.info("Updating sentiment tags for journal entries")
    for page in pages_set:
        if page.journal_entry:
            logging.info(f"Updating sentiment tags for {page.name}")
            page.Update_sentiment_tags(threshold=0.3)

    return pages_set

def main():
    # creating a connection to the database
    database = DatabaseFactory.create_database(os.getenv('DB_TYPE'))
    database.connect()

    print("Starting Logseq data extraction")

    hashtag_set = read_hashtags()
    page_set = read_pages()

    # insert all hashtags into database
    print(f"Inserting {len(hashtag_set)} hashtags into the database")
    for hashtag in hashtag_set:
        database.insert_hashtag(hashtag)
    
    # insert all pages into datase
    print(f"Inserting {len(page_set)} pages into the database")
    for page in page_set:
        database.insert_page(page)

    print("Finished Logseq data extraction")

if __name__ == "__main__":
    main()