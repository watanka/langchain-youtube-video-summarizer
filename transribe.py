import whisper
from dotenv import load_dotenv
import os

model_name = os.getenv('TRANSCRIBE_MODEL', 'base')

audiofile_path = 'input.mp3'

model = whisper.load_model(model_name)

result = model.transcribe(audiofile_path)

with open('transcription.txt', 'w') as f :
    
    f.write(result['text'])