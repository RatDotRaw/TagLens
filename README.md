# TagLens
 A Python script that analyzes Logseq files to gather and organize hashtags, providing insights into your note-taking habits and helping you discover new connections between ideas.

## Installation

### Prerequisites

> This project has only been tested on Python 3.11 and Python 3.12.

> You can get Python 3.11 or Python 3.12 from [python.org](https://www.python.org/downloads/).

1. **Create a virtual environment and activate it**
   
   You can create a virtual environment with `python3 -m venv .venv`

   Activate the virtual environment with:

   - On Windows: `.venv\Scripts\activate` (to activate the virtual environment)
   - On linux & macOS: `source .venv/bin/activate`

2. **Install the required packages**

   Run: `pip install -r requirements.txt`

## Configuration

### Selection of Database

> [!IMPORTANT]
> The Neo4j database is currently not supported for the webui.
> If you want to use the webui for visualization, you need to use SQLite.

There are currently 2 database types available:

- **SQLite**
- **Neo4j**

You can select the database type by setting the `DB_TYPE` environment variable to either `sqlite` or `neo4j`.

this is also later explained in the `Database Configuration` section.

#### Database Configuration (Neo4j)

1. **Install Neo4j**:
   If you haven't already installed Neo4j, download it from [Neo4j's official website](https://neo4j.com/download-center/#community) and follow the installation instructions for your operating system.

2. **Configure Environment Variables**:
   Ensure that the `.env` file in your project root directory is correctly configured for Neo4j. The relevant entries should look like this:

   ```env
   DB_TYPE=neo4j
   NEO4J_URL=neo4j://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=changeme
   ```
#### Database Configuration (SQLite)

> SQLite is already set up as a default option if you don't specify otherwise. SQLite will work and be used out of the box.

1. **Configure Environment Variables**:
   Ensure that the `.env` file in your project root directory is correctly configured for SQLite. The relevant entries should look like this:

   ```env
   DB_TYPE=sqlite
   SQLALCHEMY_URL = sqlite:///database.sqlite
   ```

## Usage

Before running any of the scripts, make sure you have all dependencies installed and your database is properly configured and the Virtual Environment activated.


### Scraper (Challenge 2)

> [!IMPORTANT]
> Without running the scraper first, the database will be empty and thus no data will be shown on the webui.

What does the scraper do? It reads a Logseq library and extracts all hashtags.
Then it saves them into the chosen database type.

To run the scraper, use the following command: `python scraper.py`

### WebUI (Challenge 3)

To run the webui, use the following command: `python webui.py`


## Progress

You can view the current progress and to do list in `progress.md`

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

~~Please make sure to update tests as appropriate.~~ (I wrote no tests :(, but you should! :D)

Don't know what to contribure, search for `TODO:` in the code!

## License

[Mozilla Public License 2.0](https://choosealicense.com/licenses/mpl-2.0/)