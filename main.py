import crawler as crawl

def main():
    list = crawl.crawl("/home/stafd/Documents/git/logseq/pages")
    for file in list:
        print(file.name)

if __name__ == "__main__":
    main()