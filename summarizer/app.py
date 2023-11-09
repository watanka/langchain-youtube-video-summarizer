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

app = FastAPI()


@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/summarize')
def summarize(job_id : str, transcript_path : str, summary_path : str, background_task : BackgroundTasks) : 
    runnable = Runnable(map_reduce)

    with open(transcript_path, 'r') as f :
        transcription = f.read()
    docs = text_split.split_docs(transcription)

    summary_response = runnable.invoke(docs, config = {'max_concurrency' : 4})

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
