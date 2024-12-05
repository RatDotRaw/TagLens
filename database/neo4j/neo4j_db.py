import os
import json
import logging
from classes.Page import Page
from dotenv import load_dotenv
from neo4j import GraphDatabase
from classes.Hashtag import Hashtag

load_dotenv()

class Neo4jIntegration:
    def __init__(self):
        self.driver = None

    def connect(self):
        """Establish a connection to Neo4j."""
        try:
            self.driver = GraphDatabase.driver(os.getenv("NEO4J_URL"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))
            self.driver.verify_connectivity()
            print("Connection established.")
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        """Close the connection to Neo4j."""
        if self.driver is not None:
            self.driver.close()
            logging.info("Connection closed.")

    def ensure_constraints(self):
        """Ensure necessary constraints in the database."""
        queries = [
            # Page Content constraints
            "CREATE CONSTRAINT page_name_unique IF NOT EXISTS FOR (p:Page) REQUIRE p.name IS UNIQUE",
            "CREATE CONSTRAINT hashtag_name_unique IF NOT EXISTS FOR (t:Hashtag) REQUIRE t.name IS UNIQUE",
            # Constraints on name
            "CREATE CONSTRAINT hashtag_name_unique IF NOT EXISTS FOR (h:Hashtag) REQUIRE h.name IS UNIQUE",
            "CREATE CONSTRAINT source_unique IF NOT EXISTS FOR (s:Source) REQUIRE s.path IS UNIQUE",
        ]

        with self.driver.session() as session:
            logging.info("Ensuring constraints...")
            for query in queries:
                try:
                    session.run(query)
                    logging.info(f"Executed: {query}")
                except Exception as e:
                    logging.error(f"Failed to execute: {query} with error: {e}")
        
    def insert_hashtag(self, hashtag: Hashtag):
        """
        Insert or update a hashtag in the database.

        Args:
            hashtag (Hashtag): The Hashtag object containing data to insert or update.
        """
        query = """
        MERGE (t:Hashtag {name: $name})
        ON CREATE SET 
            t.totalCount = $count,
            t.firstUsed = $first_appearance_date,
            t.lastUsed = $last_appearance_date
        ON MATCH SET
            t.totalCount = t.totalCount + $count,
            t.lastUsed = $last_appearance_date
        WITH t
        UNWIND $sources AS source_path
        MERGE (s:Source {path: source_path})
        MERGE (t)-[:APPEARS_IN]->(s)
        """

        parameters = {
            "name": hashtag.name,
            "count": hashtag.count,
            "first_appearance_date": hashtag.first_appearance_date.isoformat() if hashtag.first_appearance_date else None,
            "last_appearance_date": hashtag.last_appearance_date.isoformat() if hashtag.last_appearance_date else None,
            "sources": [source.path for source in hashtag.sources],
        }

        with self.driver.session() as session:
            try:
                session.run(query, parameters)
                logging.info(f"Inserted/Updated hashtag: {hashtag.name}")
            except Exception as e:
                logging.error(f"Failed to insert/update hashtag: {hashtag.name} with error: {e}")

    def insert_page(self, page: Page):
        """
        Insert or update a Page in the database.

        Args:
            page: The object containing data about the page to insert or update.
        """

        query = """
        MERGE (p:Page {name: $name})
        SET 
            p.fileName = $file_name,
            p.tagCount = $tag_count,
            p.wordCount = $word_count,
            p.sentimentTags = $sentiment_tags,
            p.category = $category,
            p.journalEntry = $journal_entry,
            p.date = $date
        WITH p
        UNWIND $hashtags AS hashtag_name
        MERGE (t:Tag {name: hashtag_name})
        MERGE (p)-[:CONTAINS]->(t)
        """

        parameters = {
            "name": page.name,
            "file_name": page.file.path,
            "tag_count": page.tag_count,
            "word_count": page.word_count,
            "sentiment_tags": json.dumps(page.sentiment_tags or []),  # convert sentiment_tags to JSON string
            "category": page.category or None, 
            "journal_entry": page.journal_entry,
            "date": page.date.isoformat() if page.date else None,
            "hashtags": [hashtag.name for hashtag in page.hashtags],
        }

        with self.driver.session() as session:
            try:
                session.run(query, parameters)
                logging.info(f"Inserted/Updated page: {page.name}")
            except Exception as e:
                logging.error(f"Failed to insert/update page: {page.name} with error: {e}")


neo4j_db = Neo4jIntegration()
neo4j_db.connect()
neo4j_db.ensure_constraints()
neo4j_db.close()
