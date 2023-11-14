import pytest
from pytube import YouTube
from transcriber.input_handler import InputHandler
from pytube.exceptions import VideoUnavailable
# 영상 제목
# 영상 id
# 영상 길이
# 영상 파일 사이즈 확인


    


def test_video_url() :
    # 재생목록에 있는 youtube url
    test_url = 'https://www.youtube.com/watch?v=C73XAQJFa1E&list=PLIMb_GuNnFweSpt4s8BhlN7EggZnWWqy6&index=3'
    input_handler = InputHandler()

    video_info = input_handler.parse(video_url = test_url)


    assert video_info.video_id == 'C73XAQJFa1E'
    assert video_info.video_title == '[Streamlit] EP03. 데이터프레임(DataFrame), 테이블 출력'
    assert video_info.video_length == 5*60 + 52 # 5분 52초 영상


def test_invalid_url() :
    test_url = 'https://www.youtube.com/watch?v=invalid_video_url' # invalid url
    input_handler = InputHandler()

    video_info = input_handler.parse(video_url = test_url)

    assert not video_info.is_valid 
