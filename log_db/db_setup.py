from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from log_db.db_schema import Base
import os
from dotenv import load_dotenv, find_dotenv
# 데이터베이스 엔진 생성 (예: SQLite 메모리 내 DB 사용)
load_dotenv(find_dotenv())

DB_USER = os.getenv('DB_USER', )
DB_PASSWORD = os.getenv('DB_PASSWORD', )
DB_HOST = os.getenv('DB_HOST', )
DB_PORT = os.getenv('DB_PORT', )
DB_DATABASE = os.getenv('DB_DATABASE', )


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
Base.metadata.create_all(engine)