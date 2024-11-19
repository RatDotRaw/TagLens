import tools.crawler as crawler
import tools.reader as reader

logseq_base_path = "/home/stafd/Documents/git/logseq"

def read_hashtags():
    # gather list of all files to be scanned
    journal_files = crawler.crawl(f"{logseq_base_path}/pages")
    pages_files = crawler.crawl(f"{logseq_base_path}/journals")
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


def main():
    hashtag_set = readHashtags()

if __name__ == "__main__":
    main()