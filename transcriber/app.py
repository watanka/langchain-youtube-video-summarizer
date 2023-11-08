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
def transcribe(url : str, job_id : str, background_tasks: BackgroundTasks) -> Dict[str, str] :

    # parse input url
    video_info_db = input_handler.parse(url)
    if not video_info_db.is_valid : # invalid url
        raise HTTPException(status_code = 400, detail = 'Invalid Video URL.')
    
    # 동영상 다운로드
    input_handler.download()
    
    video_info_db.job_id = job_id
    video_info_db.mp3_path = os.path.join(audio_path, f'{video_info_db.video_id}.mp3')

    # pytube 결과 저장
    background_tasks.add_task(
        background_jobs.register_pytube_result,
        job_id = video_info_db.job_id,
        is_valid = video_info_db.is_valid,
        video_id = video_info_db.video_id,
        video_title = video_info_db.video_title,
        file_size = video_info_db.file_size,
        video_length = video_info_db.video_length,
        mp3_path = video_info_db.mp3_path
    )

    transcription = yt_transcriber(video_path = video_info_db.mp3_path)
    
    # get transcription_filename
    transcript_filename = os.path.basename(os.path.splitext(video_info_db.mp3_path)[0] + '.txt')
    trscript_dir = os.getenv("TRANSCRIPTION_PATH", "transcriptions")

    trscript_path = os.path.join(trscript_dir, transcript_filename)

    with open(trscript_path, 'w') as f :
        f.write(transcription)

    # whisper 결과 저장
    background_tasks.add_task(
        background_jobs.register_whisper_result,
        job_id = job_id,
        word_count = len(transcription),
        txt_path = trscript_path        
    )


    

    return {'transcription_path' : trscript_path}

    