from log_monitoring.db_schema import Base, PyTubeInfo, WhisperInfo, MapReduceInfo
from log_monitoring.repository import PyTubeRepository, WhisperRepository, MapReduceRepository
from log_monitoring.unit_of_work import SqlAlchemyUnitOfWork

import pytest

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def in_memory_db() :
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def session_factory(in_memory_db) :
    yield sessionmaker(bind = in_memory_db,  autoflush=False, autocommit = False)

@pytest.fixture
def session(session_factory) :
    return session_factory()


def test_read_pytube_info_from_whisper_info(session) :
    test_job_id = 'test-job'

    pytube_repo = PyTubeRepository(session)
    whisper_repo = WhisperRepository(session)

    pytube_info = PyTubeInfo(
        job_id = test_job_id,
        is_valid = True,
        video_id = 'test-video',
        video_title = 'test-videotitle',
        file_size = 100,
        video_length = 30,
        mp3_path = 'audio/test.mp3',
    )

    whisper_info = WhisperInfo(
        job_id = test_job_id,
        word_count = 100,
        txt_path = 'transcriptions/test.txt',
    )

    pytube_repo.add(pytube_info)
    whisper_repo.add(whisper_info)
    session.commit()

    assert whisper_repo.get(test_job_id).pytube_info.is_valid


def test_uow_compare_wordcount_of_original_context_and_summary(session_factory) :
    uow = SqlAlchemyUnitOfWork(session_factory = session_factory)
    
    test_job_id = 'test-job'

    whisper_info = WhisperInfo(
        job_id = test_job_id,
        word_count = 500,
        txt_path = 'transcriptions/test.txt',
    )

    mapreduce_info = MapReduceInfo(
        job_id = test_job_id,
        word_count = 200,
        summary_path = 'summary/test.txt'
    )

    with uow : 
        uow.whisper_repo.add(whisper_info)
        uow.mapreduce_repo.add(mapreduce_info)
        uow.commit()

    with uow :
        query_whisper_info = uow.whisper_repo.get(job_id = test_job_id)
        query_mapreduce_info = uow.mapreduce_repo.get(job_id = test_job_id)

        assert query_whisper_info.word_count == 500
        assert query_mapreduce_info.word_count == 200


def test_pytube_info_is_not_yet_transcribed_or_summarized(session_factory) :
    uow = SqlAlchemyUnitOfWork(session_factory = session_factory)
    
    test_job_id = 'test-job'

    pytube_info = PyTubeInfo(
        job_id = test_job_id,
        is_valid = True,
        video_id = 'test-video',
        video_title = 'test-videotitle',
        file_size = 100,
        video_length = 30,
        mp3_path = 'audio/test.mp3',
    )

    with uow :
        uow.pytube_repo.add(pytube_info)
        uow.commit()

    with uow :
        query_pytube_info = uow.pytube_repo.get(job_id = test_job_id)
        assert not query_pytube_info.whisper_info

    whisper_info = WhisperInfo(
        job_id = test_job_id,
        word_count = 100,
        txt_path = 'transcriptions/test.txt',
    )

    with uow :
        uow.whisper_repo.add(whisper_info)
        uow.commit()

    with uow :
        query_pytube_info = uow.pytube_repo.get(job_id = test_job_id)

        assert query_pytube_info.whisper_info
        assert not query_pytube_info.mapreduce_info