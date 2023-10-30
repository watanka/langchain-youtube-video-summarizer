import logging
import store_data_job
from fastapi import BackgroundTasks
from pydantic import BaseModel

logger = logging.getLogger(__name__)

REDIS_QUEUE = 'redis_queue'


class SaveDataJob(BaseModel) :
    job_id : str
    src_url : str
    is_transcribed : bool = False
    is_summarized : bool = False
    content : str | None = None
    queue_name : str = REDIS_QUEUE


    def __call__(self) :
        logger.info(f'registered job: {self.job_id} in {self.__class__.__name__}')
        store_data_job.set_data_redis(self.job_id, self.src_url)
        store_data_job.left_push_queue(self.queue_name, self.job_id)
        

def save_data_job(
        src_url : str,
        job_id: str,
        background_tasks : BackgroundTasks,
        enqueue : bool = False
) -> str :
    task = SaveDataJob(
        src_url = src_url,
        job_id = job_id,
        enqueue = enqueue
    )
    background_tasks.add_task(task)

    return job_id
