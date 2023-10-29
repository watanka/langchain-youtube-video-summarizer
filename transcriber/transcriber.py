from pytube import YouTube
import os
from uuid import uuid4


class AbstractTransriber :
    pass


class YoutubeTranscriber(AbstractTransriber) :

    def __init__(self, transcribe_model) :
        self.transcribe_model = transcribe_model

    def __call__(self, video_url : str) -> str :

        # convert url to audio
        yt = YouTube(video_url)
        video_id = video_url.split('/')[-1].replace('watch?v=', '')
        audio_path = os.getenv("AUDIO_PATH", 'audios')

        # TODO match uuid with yt.title
        audio_outputpath = str(os.path.join(audio_path, f'{str(uuid4())[:4]}_{video_id}.mp3'))
        
        yt.streams.filter(only_audio=True).first().download(filename = audio_outputpath)


        result = self.transcribe_model.transcribe(audio_outputpath)

        # get transcription_filename
        transcript_filename = os.path.basename(os.path.splitext(audio_outputpath)[0] + '.txt')
        trscript_dir = os.getenv("TRANSCRIPTION_PATH", "transcriptions")

        trscript_path = os.path.join(trscript_dir, transcript_filename)

        # write to the persistant space
        with open(trscript_path, 'w') as f :
            f.write(result['text'])

        return trscript_path
