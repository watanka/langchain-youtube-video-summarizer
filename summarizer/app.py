from langchain.schema import Document
from langchain.schema.runnable import Runnable
from typing import Dict, List
from src.log_db import background_jobs

from fastapi import FastAPI, BackgroundTasks
from langserve import add_routes
import uvicorn
import text_split
from summary_chain import map_reduce
import logging
from pydantic import BaseModel

import os


logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s')

app = FastAPI()

class SummaryResult(BaseModel) :
    summary : str


@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/summarize/')
def summarize(job_id : str, transcript_path : str, summary_path : str, background_task : BackgroundTasks) -> SummaryResult: 
    logging.debug(f'received job_id[{job_id}].')
    logging.debug(f'Read transcription from {transcript_path}, current directory is {os.getcwd()}')
    with open(transcript_path, 'r') as f :
        transcription = f.read()
    logging.debug(f'job_id[{job_id}][mapreduce info] : read transcription.')
    docs = text_split.split_docs(transcription)
    logging.debug(f'job_id[{job_id}][mapreduce info] : splitted transcriptions to fit in mapreduce. \n {docs}')
    
    map_reduce.with_config(input_type = List[Document], output = SummaryResult)
    summary_result = map_reduce.invoke(docs)
    # summary_result : {'summary' : str}


    logging.debug(f'job id[{job_id}][mapreduce info] : {summary_result}')
    background_task.add_task(
        background_jobs.register_mapreduce_result,
        job_id = job_id,
        word_count = len(transcription),
        summary_path = summary_path,

    )

    background_task.add_task(
        background_jobs.save_txt,
        path = summary_path,
        context = summary_result['summary']
    )


    return summary_result
