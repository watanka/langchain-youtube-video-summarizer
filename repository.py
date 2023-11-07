from db_schema import PyTubeInfo, WhisperInfo, MapReduceInfo
from abc import ABC, abstractmethod
from typing import List, Any
from sqlalchemy.orm import Session


class AbstractRepository(ABC) :

    @abstractmethod
    def get(self, job_id : str) :
        raise NotImplementedError
    
    @abstractmethod
    def list(self) :
        raise NotImplementedError
    
    @abstractmethod
    def add(self, info : Any) :
        raise NotImplementedError
    

class PyTubeRepository(AbstractRepository) :
    def __init__(self, session : Session):
        self.session = session

    def get(self, job_id : str) -> PyTubeInfo :
        return self.session.query(PyTubeInfo).filter_by(job_id = job_id).first()

    def list(self) -> List[PyTubeInfo] :
        return list(self.session.query(PyTubeInfo).all())
    
    def add(self, pytube_info : PyTubeInfo) -> None :
        self.session.add(pytube_info)

class WhisperRepository(AbstractRepository) :
    def __init__(self, session : Session):
        self.session = session

    def get(self, job_id : str) -> WhisperInfo :
        return self.session.query(WhisperInfo).filter_by(job_id = job_id).first()

    def list(self) -> List[WhisperInfo] :
        return list(self.session.query(WhisperInfo).all())
    
    def add(self, whisper_info : WhisperInfo) -> None :
        self.session.add(whisper_info)


class MapReduceRepository(AbstractRepository) :
    def __init__(self, session : Session):
        self.session = session

    def get(self, job_id : str) -> MapReduceInfo :
        return self.session.query(MapReduceInfo).filter_by(job_id = job_id).first()

    def list(self) -> List[MapReduceInfo] :
        return list(self.session.query(MapReduceInfo).all())
    
    def add(self, mapreduce_info : MapReduceInfo) -> None :
        self.session.add(mapreduce_info)