from pytube import YouTube

class InputHandler :
    def __init__(self, parser = YouTube) :
        self.parser = parser
        self.parse_obj = None
        self.video_stream = None

        self.video_id = None
        self.video_title = None
        self.file_size = None
        self.video_length = None
    
    def parse(self, video_url : str) :
        try :
            self.parse_obj = self.parser(video_url)
        except :
            raise f'Invalid video url {video_url}'

        video_id = video_url.split('/')[-1].split('&')[0].replace('watch?v=', '')
        if not self.video_stream :
            self.video_stream = self.parse_obj.streams.filter(only_audio = True).first()
        
        self.video_id = video_id
        self.video_title = self.parse_obj.title
        self.video_length = self.parse_obj.length
        self.file_size = self.video_stream.filesize / 1024 / 1024
        

        return {
                'title' : self.video_title,
                'length' : self.video_length,
                'file_size' : self.file_size
                }
    
    def download(self) :
        if not self.parser :
            raise 'you have to parse the video first.'
        if not self.video_stream :
            self.video_stream = self.parse_obj.streams.filter(only_audio = True).first()
        
        self.video_stream.download()