from src.log_db.db_schema import PyTubeInfo, WhisperInfo, MapReduceInfo
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

    def select_complete_request_between(self, time_before : str, time_after : str) -> List[PyTubeInfo] :
        return (self.session.query(PyTubeInfo)
                            .filter(PyTubeInfo.is_valid == True)
                            .filter(PyTubeInfo.whisper_info != None)
                            .filter(PyTubeInfo.mapreduce_info != None)
                            .filter(PyTubeInfo.created_datetime >= time_before)
                            .filter(PyTubeInfo.created_datetime <= time_after)
                            .all()
                    )
    
    def select_invalid_request_between(self, time_before : str, time_after : str) -> List[PyTubeInfo] :
        return (self.session.query(PyTubeInfo)
                                .filter(PyTubeInfo.is_valid == False)
                                .filter(PyTubeInfo.created_datetime >= time_before)
                                .filter(PyTubeInfo.created_datetime <= time_after)
                                .all()
                        )
    
    def select_pending_transcription(self) -> List[PyTubeInfo] :
        '''transcription 결과가 아직 나오지 않은 valid한 url 요청'''
        return (self.session.query(PyTubeInfo)
                                .filter(PyTubeInfo.is_valid == True)
                                .filter(PyTubeInfo.whisper_info == None)
                                .all()
                )
    
    def select_pending_summarization(self) -> List[PyTubeInfo] :
        '''transcription 결과는 나왔지만, summarization 결과가 아직 나오지 않은 valid한 url 요청'''
        return (self.session.query(PyTubeInfo)
                                .filter(PyTubeInfo.is_valid == True)
                                .filter(PyTubeInfo.whisper_info != None)
                                .filter(PyTubeInfo.mapreduce_info == None)
                                .all()
                )

class WhisperRepository(AbstractRepository) :
    def __init__(self, session : Session):
        self.session = session

    def get(self, job_id : str) -> WhisperInfo :
        return self.session.query(WhisperInfo).filter_by(job_id = job_id).first()

    def list(self) -> List[WhisperInfo] :
        return list(self.session.query(WhisperInfo).all())
    
    def add(self, whisper_info : WhisperInfo) -> None :
        self.session.add(whisper_info)

    def select_info_between(self, time_before : str, time_after : str) -> List[WhisperInfo] :
        return (self.session.query(WhisperInfo)
                            .filter(WhisperInfo.created_datetime >= time_before)
                            .filter(WhisperInfo.created_datetime <= time_after)
                            .all()
                    )
    

class MapReduceRepository(AbstractRepository) :
    def __init__(self, session : Session):
        self.session = session

    def get(self, job_id : str) -> MapReduceInfo :
        return self.session.query(MapReduceInfo).filter_by(job_id = job_id).first()

    def list(self) -> List[MapReduceInfo] :
        return list(self.session.query(MapReduceInfo).all())
    
    def add(self, mapreduce_info : MapReduceInfo) -> None :
        self.session.add(mapreduce_info)

    def select_info_between(self, time_before : str, time_after : str) -> List[MapReduceInfo] :
        return (self.session.query(MapReduceInfo)
                            .filter(MapReduceInfo.created_datetime >= time_before)
                            .filter(MapReduceInfo.created_datetime <= time_after)
                            .all()
                    )