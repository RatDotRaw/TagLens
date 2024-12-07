from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

# Junction table for the many-to-many relationship between File and Hashtag
class FileHashtag(Base):
    __tablename__ = 'file_hashtags'
    
    file_id = Column(Integer, ForeignKey('Files.id'), primary_key=True)
    hashtag_id = Column(Integer, ForeignKey('hashtags.id'), primary_key=True)

class File(Base):
    __tablename__ = 'Files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    fullpath = Column(String, unique=True, nullable=False)
    
    # Many-to-Many relationship with Hashtags
    hashtags = relationship(
        'Hashtag',
        secondary='file_hashtags',
        back_populates='files'
    )

    # One-to-One relationship with Page
    page = relationship('Page', back_populates='file', uselist=False)

class Page(Base):
    __tablename__ = 'pages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    file_name = Column(String)
    tag_count = Column(Integer)
    word_count = Column(Integer)
    sentiment_tags = Column(JSON)  # Storing JSON data
    category = Column(String)
    journal_entry = Column(Text)
    date = Column(String)

    # ForeignKey for the one-to-one relationship with File
    file_id = Column(Integer, ForeignKey('Files.id'))
    file = relationship('File', back_populates='page')

class Hashtag(Base):
    __tablename__ = 'hashtags'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    total_count = Column(Integer, default=0)
    first_appearance_date = Column(String)
    last_appearance_date = Column(String)

    # Many-to-Many relationship with Files
    files = relationship(
        'File',
        secondary='file_hashtags',
        back_populates='hashtags'
    )