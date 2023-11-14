import logging
from src.backend import store_data_job
from src.backend.configurations import CacheConfigurations
from fastapi import BackgroundTasks
from pydantic import BaseModel

logger = logging.getLogger(__name__)



class SaveDataJob(BaseModel) :
    job_id : str
    src_url : str
    is_transcribed : bool = False
    is_summarized : bool = False
    content : str | None = None
    queue_name : str = CacheConfigurations.queue_name


    def __call__(self) :
        store_data_job.set_data_redis(self.job_id, self.src_url)
        pushed = store_data_job.left_push_queue(self.queue_name, self.job_id)


def save_data_job(
        src_url : str,
        job_id: str,
        background_tasks : BackgroundTasks,
        enqueue : bool = False) -> str :
    task = SaveDataJob(
        src_url = src_url,
        job_id = job_id,
    )
    background_tasks.add_task(task)

    return job_id
