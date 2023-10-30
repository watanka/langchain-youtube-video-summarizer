from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()


class SaveDataJob(Base) :
    __tablename__ = 'savedatajobs'

    job_id = Column(String, primary_key=True)
    src_url = Column(String, nullable=False)
    is_transcribed = Column(Boolean, default=False)
    is_summarized = Column(Boolean, default=False)
    content = Column(String)

engine = create_engine(url = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER', 'test-user'),
    os.getenv('DB_PASSWORD', 'test1234'),
    os.getenv('DB_HOST', 'db-server'),
    os.getenv('DB_PORT', '3306'),
    os.getenv('DB_DATABASE', 'savedatajob'),
))
Session = sessionmaker(bind = engine)
session = Session()

Base.metadata.create_all(engine, check_first = True)


class DataJobRepository :
    
    def __init__(self, session) :
        self.session = session

    def get(self, job_id : str) -> SaveDataJob :
        return self.session.query(SaveDataJob).filter_by(job_id = job_id).first()

    def add(self, datajob : SaveDataJob) :
        self.session.add(datajob)

    def list(self) :
        return self.session.query(SaveDataJob).all()