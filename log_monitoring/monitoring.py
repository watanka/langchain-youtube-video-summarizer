from src.log_db.unit_of_work import SqlAlchemyUnitOfWork
from src.log_db.db_setup import session
from src.log_db.db_schema import PyTubeInfo

from typing import List

uow = SqlAlchemyUnitOfWork(session)

# invalid request
def invalid_request(time_before : str, time_after : str) -> List[PyTubeInfo] :
    with uow :
        return uow.pytube_repo.select_invalid_request_between(time_before, time_after)

def complete_request(time_before : str, time_after : str) -> List[PyTubeInfo] : 
    with uow :
        return uow.pytube_repo.select_complete_request_between(time_before, time_after)


def pending_transcription() :
    with uow :
        return uow.pytube_repo.select_pending_transcription()

def pending_summarization() :
    with uow :
        return uow.pytube_repo.select_pending_summarization()

