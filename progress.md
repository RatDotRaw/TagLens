# Data Collected by My LogSeq Journal Scraper

## saving data into database

- [ ] research what database to use (neo4j, NetworkX (serverless), simple csv)
  - [ ] save gathered data in database


## Technical

- [ ] Move Tag specific logic from function into the `Hashtag` class

## Page Content

Why is info of page content gathered? it might give more context to each tag. What its used for, when its used, why and so on.

- [ ] Page title
- [x] Tags in pages.
- [x] Count of tags used in page
- [x] Count of all words (except tags)
- [x] Count of unique tags per page
- [x] sentiment analysis of the page content using a pre-trained model.
- [ ] category of the page (e.g., work, personal, etc.)

## Tags

Why gather info of tags? In my final projecta application, I am going to make a tagging application. For a better user experience i want to have a solid choise of pre made tags. Another reason, There are going to be tags with extra functionality, like a tag that triggers a reminder. I hope to find more use cases and insights by gathering info.

- [x] Tag name
- [x] Total count of tag
- [x] Source of where the tag was found (path to the file)
  - [x] Count of notes for the tag
- [x] Date when the tag was first used in a note
- [x] Date when the tag was last used in a note
