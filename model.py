#bills
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine("sqlite:///tweets.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))
Base = declarative_base()
Base.query = session.query_property()

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key = True)
    username = Column(String(64), nullable=False)
    user_image = Column(String(100), nullable=False)
    text = Column(String(140), nullable=False)
    id_num = Column(Integer, nullable=False)
    date = Column(String(64), nullable = False)
    read = Column(String(1), nullable = False)


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()