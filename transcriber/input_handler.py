from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from log_db.db_schema import PyTubeInfo

from pydantic import BaseModel
import re

from logging import getLogger

logger = getLogger(__name__)

class PytubeParseError(Exception) :
    pass 

class InvalidURLError(Exception) :
    pass




class InputHandler :
    def __init__(self, parser = YouTube) :
        self.parser = parser
        self.parse_obj = None
        self.video_stream = None
        # 필요한 정보
        self.is_valid = False
        self.video_id = None
        self.video_title = None
        self.file_size = None
        self.video_length = None
    
    def parse(self, video_url : str) :
        
        try :
            self.parse_obj = self.parser(video_url)
            self.parse_obj.check_availability()
            self.is_valid = True

        except :
            logger.debug(f'Invalid url {video_url}')

            
        else : 
            video_id_match = re.search(r"v=([^&#]+)", video_url)
            ## TODO
            video_id = video_id_match.group(1) if video_id_match else None

            if not self.video_stream :
                self.video_stream = self.parse_obj.streams.filter(only_audio = True).first()
            
            self.video_id = str(video_id)
            self.video_title = self.parse_obj.title
            self.video_length = self.parse_obj.length
            self.file_size = self.video_stream.filesize / 1024 / 1024
        

        return PyTubeInfo(**{
                'is_valid' : self.is_valid,
                'video_id' : self.video_id,
                'video_title' : self.video_title,
                'file_size' : self.file_size,
                'video_length' : self.video_length,
                })
    
    def download(self, mp3_path : str) :
        if not self.parse_obj :
            raise PytubeParseError('you have to parse the video first.')
        if not self.video_stream :
            self.video_stream = self.parse_obj.streams.filter(only_audio = True).first()
        
        self.video_stream.download(output_path=mp3_path)