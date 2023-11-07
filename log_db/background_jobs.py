from log_db.db_schema import PyTubeInfo, WhisperInfo, MapReduceInfo
from log_db.db_setup import session
from log_db.unit_of_work import SqlAlchemyUnitOfWork

uow = SqlAlchemyUnitOfWork(session)

def register_pytube_result(
        job_id : str,
        is_valid : bool,
        video_id : str,
        video_title : str,
        file_size : float,
        video_length : int,
        mp3_path : str
) : 
    pytube_info = PyTubeInfo(
        job_id = job_id,
        is_valid = is_valid,
        video_id = video_id,
        video_title = video_title,
        file_size = file_size,
        video_length = video_length,
        mp3_path = mp3_path,
    )

    with uow :
        uow.pytube_repo.add(pytube_info)
        uow.commit()
    

def register_whisper_result(
        job_id : str,
        word_count : int,
        txt_path : str
) :
    whisper_info = WhisperInfo(
        job_id = job_id,
        word_count = word_count,
        txt_path = txt_path
    )
    
    with uow :
        uow.whisper_repo.add(whisper_info)
        uow.commit()

def register_mapreduce_result(
        job_id : str,
        word_count : int,
        summary_path : str
) :
    mapreduce_info = MapReduceInfo(
        job_id = job_id,
        word_count = word_count,
        summary_path = summary_path
    )
    
    with uow :
        uow.mapreduce_repo.add(mapreduce_info)
        uow.commit()


def save_txt(path : str, context : str) :
    with open(path, 'w') as f :
        f.write(context)