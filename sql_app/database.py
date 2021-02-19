import json
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

try:
    with open(os.getcwd() + '/env.json') as f:
        data = json.load(f)
        SQL_ALCHEMY_DATABASE_URL = data['db_url']
except FileNotFoundError:
    exit(-1)

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
