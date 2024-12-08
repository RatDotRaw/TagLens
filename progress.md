# Data Collected by My LogSeq Journal Scraper

## Scraper (challenge 2)

### saving data into database

- [x] research what database to use (neo4j, NetworkX (serverless), simple csv)
  - [x] save gathered data in database
  - [x] extra: save data in sqlite database

I chose for neo4j because it is a graph database that can handle the complexity of my data. it also has a web interface that allows me to visualize the data in a graph format and query the data in a graph format.

- I didn't really use the full potential of neo4j database. So I decided to also save the data in a SQLite database for easier use and familiarity.

### Technical

A list of techical stuff I want to do next to clean up the project:

- [x] Move Tag specific logic from function into the `Hashtag` class

### Page Content

Why is info of page content gathered? it might give more context to each tag. What its used for, when its used, why and so on.

- [ ] Page title
- [x] Tags in pages.
- [x] Count of tags used in page
- [x] Count of all words (except tags)
- [x] Count of unique tags per page
- [x] sentiment analysis of the page content using a pre-trained model.
- [ ] category of the page (e.g., work, personal, etc.)

### Tags

Why gather info of tags? In my ~~final projecta application, I am going to make a tagging application.~~ For a better user experience i want to have a solid choise of pre made tags. Another reason, There are going to be tags with extra functionality, like a tag that triggers a reminder. I hope to find more use cases and insights by gathering info. another personal reason is that I want to have a better understanding of my own tagging habits, what tags I use most, which one is too granular or nieche and so on... ~~to maybe in the future clean up a bit.~~ <-- (lying to myself)

- [x] Tag name
- [x] Total count of tag
- [x] Source of where the tag was found (path to the file)
  - [x] Count of notes for the tag
- [x] Date when the tag was first used in a note
- [x] Date when the tag was last used in a note