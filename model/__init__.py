from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import mysql.connector

from config import DATABASE_URL, MYSQL_CONNECT_KWARGS, SQLALCHEMY_ECHO

Base = declarative_base()

engine = create_engine(
    DATABASE_URL,
    echo=SQLALCHEMY_ECHO,
    pool_pre_ping=True,
)

Session = sessionmaker(bind=engine)
session = Session()

mydb = mysql.connector.connect(**MYSQL_CONNECT_KWARGS)
