from fastapi import FastAPI
from transcription import YoutubeTranscriber

from logging import getLogger

from typing import Dict
from dotenv import load_dotenv
import whisper
import os
import torch

logger = getLogger(__name__)

model_name = os.getenv('TRANSCRIBE_MODEL', 'tiny')
audiofile_path = 'input.mp3'
logger.debug('loading whisper model')

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = whisper.load_model('tiny', device = device)
logger.debug('whisper model ready')



app = FastAPI()

yt_transcriber = YoutubeTranscriber(transcribe_model = model)

@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/transcribe/')
def transcribe(url : str) -> Dict[str, str] :

    trscript_path = yt_transcriber(video_url = url)

    return {'transcription_path' : trscript_path}

    