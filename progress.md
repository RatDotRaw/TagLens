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

Why gather info of tags? In my ~~final projecta application, I am going to make a tagging application. For a better user experience i want to have a solid choise of pre made tags. Another reason, There are going to be tags with extra functionality, like a tag that triggers a reminder. I hope to find more use cases and insights by gathering info.~~ To find


another personal reason is that I want to have a better understanding of my own tagging habits, what tags I use most, which one is too granular or nieche and so on... ~~to maybe in the future clean up a bit.~~ <-- (lying to myself)

- [x] Tag name
- [x] Total count of tag
- [x] Source of where the tag was found (path to the file)
  - [x] Count of notes for the tag
- [x] Date when the tag was first used in a note
- [x] Date when the tag was last used in a note

## webui (Challenge 3)

### Technical Checklist:

- [x] Set up a basic Flask project structure:

  Think a bit ahead of how the project structure is going to be structured. Think about how you will organize your routes, templates, static files, and other components.

- [ ] Prepare a list of data to be visualized:

  Quickly list out the data that you want to visualize. This could include counts of tags, sentiment analysis results, page titles, etc.

  information visualized on the webui:
    - Tag name

- [ ] Implement the web application logic:
  - [ ] Create view functions in `views.py` to handle requests and responses.
  - [ ] Create templates in the `templates` directory for HTML rendering.
  
- [ ] Connect the web application to the database:
  - [ ] Use SQLAlchemy or other ORM to interact with the SQLite database.
  - ~~[ ] Use Neo4j with py2neo to interact with the Neo4j database.~~ (no more neo4j, sqlite database has been chosen and is more structured)
  - [ ] Create models to represent entities (e.g., Tag, Page).

- [ ] Implement data retrieval and display:
  - [ ] Fetch data from the database using the Flask route handlers.
  - [ ] Pass data to the templates for rendering.

- [ ] Enhance user experience:
  - [ ] Display analytics and insights in a visually appealing manner (e.g., charts, graphs).
