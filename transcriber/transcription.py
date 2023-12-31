from pytube import YouTube
import os
from uuid import uuid4


class AbstractTransriber :
    pass

class FakeTranscribeModel :
    def transcribe(self, video_path : str) :
        return {'text' : f'Given {video_path}, BUT THIS IS FAKE TRANSCRIPTION.'}

class YoutubeTranscriber(AbstractTransriber) :

    def __init__(self, transcribe_model) :
        self.transcribe_model = transcribe_model

    def __call__(self, video_path : str) -> str :
        result = self.transcribe_model.transcribe(video_path)

        return result['text']
