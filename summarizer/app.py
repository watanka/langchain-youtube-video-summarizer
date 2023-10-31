from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from mapreduce_langchain import mapreduce_transcript


app = FastAPI()


@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/summarize/')
def summarize(transcript_path : str) -> Dict[str, str] :
    with open(transcript_path, 'r') as f :
        transcription = f.read()
    
    sum_result = mapreduce_transcript(transcription)
    return {'summary' : sum_result}
