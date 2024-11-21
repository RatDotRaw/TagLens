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
    
    # fill in file dates

    # loop trough hastags and set dates
    for hashtag in hashtag_set:
        sources = hashtag.sources
        for source in sources:
            # TODO: loop over source list and find first and last date
            date = crawler.get_page_date(source.name)
            if date:
                # check if the date is newer than the current first appearance or older than the last appearance
                if hashtag.first_appearance_date is None or date < hashtag.first_appearance_date:
                    hashtag.first_appearance_date = date

                if hashtag.last_appearance_date is None or date > hashtag.last_appearance_date:
                    hashtag.last_appearance_date = date
    return hashtag_set
    # print out all info from hashtags
    # for hashtag in hashtag_set:
    #     print("#"*50)
    #     print("name:", hashtag.name)
    #     print("count:", hashtag.count)
    #     print("total sources:", len(hashtag.sources))
    #     print("first appearance date:", hashtag.first_appearance_date)
    #     print("last appearance date:", hashtag.last_appearance_date)

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
    # hashtag_set = read_hashtags()
    page_set = read_pages()
    

if __name__ == "__main__":
    main()