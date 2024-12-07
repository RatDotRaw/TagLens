import json
import os
import logging

from classes.File import File as FileClass
from classes.Page import Page as PageClass
from classes.Hashtag import Hashtag as HashtagClass
from .models import Base
from .models import File
from .models import Page
from .models import Hashtag
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

class SqliteIntegration:
    def __init__(self):
        self.sessionLocal = None
    
    def connect(self):
        """Establish a connection to the sqlite database."""
        try:
            # create engine to connect to the database
            engine = create_engine(os.getenv("SQLALCHEMY_URL"), echo=False, pool_pre_ping=False)
            # create all teh tables based on the base class
            Base.metadata.create_all(bind=engine)
            self.sessionLocal = sessionmaker(bind=engine, autoflush=False)
            
            print("Connection established.")
        except Exception as e:
            print(f"Failed to connect to database: {e}")
            raise
    
    def close(self):
        """Close teh connection to the databse"""
        if self.sessionLocal:
            self.sessionLocal.close_all()
            self.sessionLocal = None

    def insert_file(self, file: FileClass):
        """
        Inserts if not exist a File record in the database.

        Args:
            session (Session): SQLAlchemy session.
            file (File): File class containing all the data.
        """
        try:
            session = self.sessionLocal()
            # Check if the file exists
            db_file = session.query(File).filter_by(fullpath=file.fullpath).first()

            if not db_file:
                # Insert a new record
                db_file = File(
                    name=file.name, 
                    fullpath=file.fullpath
                )
                session.add(db_file)
            else:
                logging.warning(f"File already exists: {file.fullpath}")
            
            # Commit changes
            session.commit()
            return db_file
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to insert file: {e}")
        finally:
            session.close()

    def insert_hashtag(self, hashtag: HashtagClass):
        """
        Insert or update a hashtag in the database.

        Args:
            session (Session): SQLAlchemy session to interact with the database.
            hashtag (Hashtag): The Hashtag object containing data to insert or update.
        """
        try:
            session = self.sessionLocal()

            # Check if the hashtag exists
            db_hashtag = session.query(Hashtag).filter_by(name=hashtag.name).first()

            if db_hashtag is None:
                # Insert new hashtag
                db_hashtag = Hashtag(
                    name=hashtag.name,
                    total_count=hashtag.count,
                    first_appearance_date=hashtag.first_appearance_date,
                    last_appearance_date=hashtag.last_appearance_date,
                )
                session.add(db_hashtag)
            else:
                # Update existing hashtag
                db_hashtag.count = hashtag.count
                db_hashtag.first_appearance_date = hashtag.first_appearance_date  # Fixed here
                db_hashtag.last_appearance_date = hashtag.last_appearance_date  # Fixed here

            # Link file and hashtag
            for file in hashtag.sources:
                db_file = session.query(File).filter_by(fullpath=file.fullpath).first()
                if not db_file:
                    # Insert a new file record if it doesn't exist
                    db_file = self.insert_file(file)
                    db_file = session.query(File).filter_by(fullpath=file.fullpath).first()  # Fetch the inserted file

                # Link the existing or newly inserted file with the hashtag
                if db_file and db_hashtag:
                    # Many-to-many relationship: add the hashtag to the file's hashtags list
                    if db_hashtag not in db_file.hashtags:
                        db_file.hashtags.append(db_hashtag)

            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to insert/update hashtag: {hashtag.name} with error: {e}")

    # def insert_page(self, page: PageClass):
    #     """
    #     Insert or update a page in the database.

    #     Args:
    #         session (Session): SQLAlchemy session to interact with the database.
    #         page (Page): The Page object containing data to insert or update.
        
    #     """
    #     try:
    #         session = self.sessionLocal()

    #         # Check if the page exists
    #         db_page = session.query(Page).filter_by(name=page.name).first()

    #         if db_page is None:
    #             # Insert new page
    #             db_page = Page(
    #                 name = page.name,
    #                 file_name = page.file.name,
    #                 tag_count = page.tag_count, 
    #                 word_count = page.word_count,
    #                 sentiment_tags = json.dumps(page.sentiment_tags),
    #                 category= page.category,
    #                 journal_entry = page.journal_entry,
    #                 date = page.date
    #             )
    #             session.add(db_page)
    #         else:
    #             # Update existing page
    #             db_page.tag_count = page.tag_count
    #             db_page.word_count = page.word_count
    #             db_page.sentiment_tags = json.dumps(page.sentiment_tags)
    #             db_page.category = page.category
    #             db_page.journal_entry = page.journal_entry
    #             db_page.date = page.date
            
    #         # Link file to page
    #         db_file = session.query(File).filter_by(fullpath=page.file.fullpath).first()
    #         if not db_file:
    #             # Insert a new file record if it doesn't exist
    #             self.insert_file(page.file)
    #             db_file = session.query(File).filter_by(fullpath=page.file.fullpath).first()  # Fetch the inserted file

    #         # Link the existing or newly inserted file with the page
    #         if db_file and db_page:
    #             # one-to-one relationship: set the file for the page
    #             db_page.file_id = db_file.id

    #         session.commit()
    #     except SQLAlchemyError as e:
    #         session.rollback()
    #         raise ValueError(f"Failed to insert/update page: {page.name} with error: {e}")



    def insert_page(self, page: PageClass):
        """
        Insert or update a page in the database.

        Args:
            session (Session): SQLAlchemy session to interact with the database.
            page (Page): The Page object containing data to insert or update.

        """
        try:
            session = self.sessionLocal()

            # Check if the page exists
            db_page = session.query(Page).filter_by(name=page.name).first()

            if db_page is None:
                # Insert new page
                db_page = Page(
                    name = page.name,
                    file_name = page.file.name,
                    tag_count = page.tag_count, 
                    word_count = page.word_count,
                    sentiment_tags = json.dumps(page.sentiment_tags) if page.sentiment_tags else None,  # Ensure None if empty
                    category= json.dumps(page.sentiment_tags) if page.sentiment_tags else None,
                    journal_entry = page.journal_entry,
                    date = page.date
                )
                session.add(db_page)
            else:
                # Update existing page
                db_page.tag_count = page.tag_count
                db_page.word_count = page.word_count
                db_page.sentiment_tags = json.dumps(page.sentiment_tags) if page.sentiment_tags else None  # Ensure None if empty
                db_page.category = json.dumps(page.sentiment_tags) if page.sentiment_tags else None  # Ensure None if empty
                db_page.journal_entry = page.journal_entry
                db_page.date = page.date

            # Link file to page
            db_file = session.query(File).filter_by(fullpath=page.file.fullpath).first()
            if not db_file:
                # Insert a new file record if it doesn't exist
                self.insert_file(page.file)
                db_file = session.query(File).filter_by(fullpath=page.file.fullpath).first()  # Fetch the inserted file

            # Link the existing or newly inserted file with the page
            if db_file and db_page:
                # one-to-one relationship: set the file for the page
                db_page.file_id = db_file.id

            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError(f"Failed to insert/update page: {page.name} with error: {e}")
