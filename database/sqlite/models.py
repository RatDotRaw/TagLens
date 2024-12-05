from typing import List
from typing import Optional
from sqlalchemy import String
from sqlalchemy import Column, Integer, String, Text, Date, JSON, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

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
    date = Column(Date)

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
    date = Column(Date)