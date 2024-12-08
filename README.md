# TagLens
 A Python script that analyzes Logseq files to gather and organize hashtags, providing insights into your note-taking habits and helping you discover new connections between ideas.

## Installation

### Prerequisites

* This project has only been tested on Python 3.11.

### Step 1: Create a virtual environment and install the required packages

`python3 -m venv .venv`

### Step 2: Activate the virtual environment (optional, but recommended)

1. On Windows: `.venv\Scripts\activate` (to activate the virtual environment)
2. On linux & macOS: `source .venv/bin/activate`

### Step 3: Install the required packages

1. Run: `pip install -r requirements.txt`

## Usage

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