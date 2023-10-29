from fastapi import FastAPI, BackgroundTasks
from transcription import YoutubeTranscriber

from uuid import uuid4
from typing import Dict
from dotenv import load_dotenv
import whisper
import os
import torch

model_name = os.getenv('TRANSCRIBE_MODEL', 'tiny')
audiofile_path = 'input.mp3'
print('loading whisper model')

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = whisper.load_model('tiny', device = device)
print('whisper model ready')



app = FastAPI()

yt_transcriber = YoutubeTranscriber(transcribe_model = model)

@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/transcribe/')
def transcribe(url : str, background_tasks : BackgroundTasks) -> Dict[str, str] :

    trscript_path = yt_transcriber(video_url = url)
    
    job_id = str(uuid4())[:6]

    return {'job_id' : job_id}
    return {'transcription_path' : trscript_path}

    