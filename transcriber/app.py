from fastapi import FastAPI, BackgroundTasks, HTTPException
from transcription import YoutubeTranscriber
from log_db import background_jobs

from logging import getLogger
from transcriber.input_handler import InputHandler
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

audio_path = os.getenv("AUDIO_PATH", 'audios')

app = FastAPI()

input_handler = InputHandler()
yt_transcriber = YoutubeTranscriber(transcribe_model = model)

@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/transcribe/')
def transcribe(url : str, job_id : str, background_tasks : BackgroundTasks) -> Dict[str, str] :

    # parse input url
    video_info_db = input_handler.parse(url)
    if not video_info_db.is_valid : # invalid url
        raise HTTPException(status_code = 400, detail = 'Invalid Video URL.')
    
    # 동영상 다운로드
    input_handler.download()
    
    video_info_db.job_id = job_id
    video_info_db.mp3_path = os.path.join(audio_path, f'{video_info_db.video_id}.mp3')

    trscript_path = yt_transcriber(video_path = video_info_db.mp3_path)

    # TODO background로 값 db에 집어넣기
    

    return {'transcription_path' : trscript_path}

    