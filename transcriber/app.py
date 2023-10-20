from fastapi import FastAPI

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

@app.get('/health')
def health() -> Dict[str, str]:
    return {"health": "ok"}


@app.post('/transcribe/')
def transcribe(audiofile_path : str) -> Dict[str, str] :
    result = model.transcribe(audiofile_path)

    trsript_fname = os.path.basename(os.path.splitext(audiofile_path)[0] + '.txt')

    trscript_dir = os.getenv("TRANSCRIPTION_PATH", "transcriptions")

    trscript_path = os.path.join(trscript_dir, trsript_fname)
    with open(trscript_path, 'w') as f :
        f.write(result['text'])

    return {'transcription_path' : trscript_path}

    