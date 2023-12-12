from fastapi import FastAPI, BackgroundTasks, HTTPException
from transcription import YoutubeTranscriber, FakeTranscribeModel
from src.log_db import background_jobs

import logging


from input_handler import InputHandler
from typing import Dict
from dotenv import load_dotenv

import os

logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s')



env_setting = os.getenv('ENVIRONMENT')
logging.info(f'ENVIRONMENT : {env_setting}')
if env_setting == 'production' :
    import whisper
    import torch
    model_name = os.getenv('TRANSCRIBE_MODEL', 'tiny')
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    model = whisper.load_model('tiny', device = device)
    logging.debug(f'[OPENAI Whisper] model version [{model_name}] loaded. Using device [{device}].')
    
elif env_setting == 'test' :
    model = FakeTranscribeModel() 
    logging.debug('[Fake Transcription] model loaded. Results are FAKE!')


audio_path = os.getenv("AUDIO_PATH", 'audios')

app = FastAPI()

input_handler = InputHandler()
yt_transcriber = YoutubeTranscriber(transcribe_model = model)

@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/transcribe/')
def transcribe(url : str, job_id : str, background_tasks: BackgroundTasks):

    # parse input url
    video_info_db = input_handler.parse(url)
    if not video_info_db.is_valid : # invalid url
        raise HTTPException(status_code = 400, detail = 'Invalid Video URL.')
    
    video_info_db.job_id = job_id
    video_filename = f'{video_info_db.video_id}.mp3'
    # 동영상 다운로드
    input_handler.download(folder_dir = audio_path, filename = video_filename)
    
    video_info_db.mp3_path = os.path.join(audio_path, video_filename)
    
    # pytube 결과 저장
    
    logging.debug(f'job id[{job_id}][pytube info] : {video_info_db.__dict__}')
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

    # whisper 결과 저장
    logging.debug(f'job id[{job_id}][whisper info] : {transcription}')
    background_tasks.add_task(
        background_jobs.register_whisper_result,
        job_id = job_id,
        word_count = len(transcription),
        txt_path = trscript_path        
    )

    background_tasks.add_task(
        background_jobs.save_txt,
        path = trscript_path,
        context = transcription
    )

    return {'transcription_path' : trscript_path,
            'video_id' : video_info_db.video_id
            }

    