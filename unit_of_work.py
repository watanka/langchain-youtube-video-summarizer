from repository import PyTubeRepository, WhisperRepository, MapReduceRepository
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class AbstractUnitOfWork(ABC):
    pytube_repo : PyTubeRepository
    whisper_repo : WhisperRepository
    mapreduce_repo : MapReduceRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
    

class SqlAlchemyUnitOfWork(AbstractUnitOfWork) :
    pytube_repo : PyTubeRepository
    whisper_repo : WhisperRepository
    mapreduce_repo : MapReduceRepository

    def __init__(self, session_factory : Session) :
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.pytube_repo = PyTubeRepository(self.session)
        self.whisper_repo = WhisperRepository(self.session)
        self.mapreduce_repo = MapReduceRepository(self.session)
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self) :
        self.session.commit()

    def rollback(self) :
        self.session.rollback()