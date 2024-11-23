import os
from dotenv import load_dotenv
import logging
from neo4j import GraphDatabase
from classes.Page import Page

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
            "CREATE CONSTRAINT page_title_unique IF NOT EXISTS FOR (p:Page) REQUIRE p.title IS UNIQUE",
            "CREATE CONSTRAINT tag_name_unique IF NOT EXISTS FOR (t:Tag) REQUIRE t.name IS UNIQUE",
            # Indexes for performance optimization
            "CREATE INDEX page_tags_index IF NOT EXISTS FOR (p:Page) ON (p.tags)",
            "CREATE INDEX page_word_count_index IF NOT EXISTS FOR (p:Page) ON (p.wordCount)",
            "CREATE INDEX page_unique_tags_count_index IF NOT EXISTS FOR (p:Page) ON (p.uniqueTagsCount)",
            "CREATE INDEX page_sentiment_index IF NOT EXISTS FOR (p:Page) ON (p.sentiment)",
            # Tags-specific constraints and indexes
            "CREATE INDEX tag_total_count_index IF NOT EXISTS FOR (t:Tag) ON (t.totalCount)",
            "CREATE CONSTRAINT source_path_unique IF NOT EXISTS FOR (s:Source) REQUIRE s.path IS UNIQUE",
            "CREATE INDEX tag_first_used_date_index IF NOT EXISTS FOR (t:Tag) ON (t.firstUsed)",
            "CREATE INDEX tag_last_used_date_index IF NOT EXISTS FOR (t:Tag) ON (t.lastUsed)"
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
        MERGE (t:Tag {name: $name})
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

