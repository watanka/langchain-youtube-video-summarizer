from pytube import YouTube
import os
from uuid import uuid4


class AbstractTransriber :
    pass


class YoutubeTranscriber(AbstractTransriber) :

    def __init__(self, transcribe_model) :
        self.transcribe_model = transcribe_model

    def __call__(self, video_path : str) -> str :
        result = self.transcribe_model.transcribe(video_path)

        # get transcription_filename
        transcript_filename = os.path.basename(os.path.splitext(video_path)[0] + '.txt')
        trscript_dir = os.getenv("TRANSCRIPTION_PATH", "transcriptions")

        trscript_path = os.path.join(trscript_dir, transcript_filename)

        # write to the persistant space
        with open(trscript_path, 'w') as f :
            f.write(result['text'])

        return trscript_path
