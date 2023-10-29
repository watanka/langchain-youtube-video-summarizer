import logging

from fastapi import BackgroundTasks
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class SaveDataJob(BaseModel) :
    job_id : str
    src_url : str
    is_transcribed : bool
    is_summarized : bool
    content : str | None


    def __call__(self) :
        logger.info(f'registered job: {self.job_id} in {self.__class__.__name__}')
        