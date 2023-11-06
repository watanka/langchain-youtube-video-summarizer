from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PyTubeInfo(Base):
    __tablename__ = 'pytube_info'
    id = Column(Integer, primary_key=True, autoincrement = True)  # 기본키
    is_valid = Column(Boolean, nullable=False)
    video_id = Column(String(15), nullable=False)  
    video_title = Column(String(255), nullable=False)  
    video_length = Column(Integer, nullable=False)
    file_size = Column(Float, nullable=False)
    mp3_path = Column(String(255), nullable=True)  # 파일 경로의 길이에 따라 적절하게 조정
