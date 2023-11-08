from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.schema.runnable import Runnable
from typing import Dict, List
from log_db import background_jobs

from fastapi import FastAPI, BackgroundTasks
from langserve import add_routes
import uvicorn
import text_split
from summary_chain import map_reduce
from logging import getLogger

logger = getLogger(__name__)


app = FastAPI()


@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/summarize')
def summarize(job_id : str, transcript_path : str, summary_path : str, background_task : BackgroundTasks) : 
    
    runnable = Runnable(map_reduce)
    logger.info('runnable set')
    with open(transcript_path, 'r') as f :
        transcription = f.read()
    docs = text_split.split_docs(transcription)
    logger.info('Load transcription.')
    summary_response = runnable.invoke(docs, config = {'max_concurrency' : 4})
    logger.info(f'runnable done. response is {summary_response}')
    background_task.add_task(
        background_jobs.register_mapreduce_result,
        job_id = job_id,
        word_count = len(transcription),
        summary_path = summary_path,

    )

    background_task.add_task(
        background_jobs.save_txt,
        path = summary_path,
        context = summary_response
    )

    return summary_response



add_routes(
    app,
    map_reduce,
    path = '/mapreduce',
    input_type = List[Document],
    config_keys = {}
)


if __name__ == '__main__' :
    uvicorn.run(app, host = '127.0.0.1', port = 6500)