from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()



class PyTubeInfo(Base):
    __tablename__ = 'pytube_info'
    job_id = Column(String(15), primary_key=True, nullable = False)

    is_valid = Column(Boolean, nullable=False)
    video_id = Column(String(15), nullable=False)  
    video_title = Column(String(255), nullable=False)  
    video_length = Column(Integer, nullable=False)
    file_size = Column(Float, nullable=False)
    mp3_path = Column(String(255), nullable=True)  # 파일 경로의 길이에 따라 적절하게 조정
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    whisper_info = relationship('WhisperInfo', back_populates='pytube_info', uselist = False)
    mapreduce_info = relationship('MapReduceInfo', back_populates='pytube_info', uselist = False)



class WhisperInfo(Base) :
    __tablename__ = 'whisper_info'
    id = Column(Integer, primary_key=True, autoincrement = True)  # 기본키
    job_id = Column(String(15), ForeignKey('pytube_info.job_id'))
    word_count = Column(Integer, nullable = True)
    txt_path = Column(String(255), nullable = True)
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )

    pytube_info = relationship('PyTubeInfo', back_populates = 'whisper_info', uselist = False)
    # mapreduce_info = relationship('MapReduceInfo', back_populates = 'whisper_info', uselist = False)



class MapReduceInfo(Base) :
    __tablename__ = 'mapreduce_info'
    id = Column(Integer, primary_key=True, autoincrement = True)  # 기본키
    job_id = Column(String(15), ForeignKey('pytube_info.job_id'))
    word_count = Column(Integer, nullable = True)
    summary_path = Column(String(255), nullable = True)
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )
    pytube_info = relationship('PyTubeInfo', back_populates = 'mapreduce_info', uselist = False)
    # whisper_info = relationship('WhisperInfo', back_populates = 'mapreduce_info', uselist = False)