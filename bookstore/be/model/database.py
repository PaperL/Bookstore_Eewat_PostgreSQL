# print('INIT:\tdatabase.py')
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url, pool_size=10000)
        self.Session = sessionmaker(bind=self.engine)
        self.base = declarative_base()

    def create_session(self) -> Session:
        return self.Session()
    
    def clear_session(self):
        self.engine.dispose()


database_instance = Database(
    'postgresql://postgres:123456@localhost:5432/bookstore')


def init_database():
    # print('INIT:\tinit_database()')
    database_instance.base.metadata.create_all(database_instance.engine)


def getDatabase() -> Database:
    return database_instance


def getDatabaseBase():
    return database_instance.base


def getDatabaseSession() -> Session:
    return database_instance.create_session()

def clearDatabaseSession():
    database_instance.clear_session()