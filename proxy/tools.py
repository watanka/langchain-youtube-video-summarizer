from pytube import YouTube
import os
from uuid import uuid4

def convert_video2audio(video_url : str ) :
    
    yt = YouTube(video_url)

    video_id = video_url.split('/')[-1].replace('watch?v=', '')
    audio_path = os.getenv("AUDIO_PATH", 'audios')

    # TODO match uuid with yt.title
    audio_outputpath = str(os.path.join(audio_path, f'{str(uuid4())[:4]}_{video_id}.mp3'))
    
    yt.streams.filter(only_audio=True).first().download(filename = audio_outputpath)

    return audio_outputpath

