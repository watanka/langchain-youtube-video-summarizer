from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.log_db.db_schema import Base
import os
from dotenv import load_dotenv, find_dotenv
# 데이터베이스 엔진 생성 (예: SQLite 메모리 내 DB 사용)
load_dotenv(find_dotenv())

DB_USER = os.getenv('DB_USER', 3306)
DB_PASSWORD = os.getenv('DB_PASSWORD', 'test1234')
DB_HOST = os.getenv('DB_HOST', 'logging-db')
DB_PORT = os.getenv('DB_PORT', 3306)
DB_DATABASE = os.getenv('DB_DATABASE', 'log_info')


DATABASE_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_DATABASE
)


engine = create_engine(DATABASE_URL)
session = sessionmaker(bind = engine, autoflush = False, autocommit = False)
# 테이블 생성
Base.metadata.create_all(engine, checkfirst = True)

def get_db() :
    db = session()
    try : 
        yield db
    finally : 
        db.close()