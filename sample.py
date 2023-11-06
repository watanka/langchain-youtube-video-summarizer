import streamlit as st
import requests

st.title('Langchain Youtube Summarizer:sunglasses:')


url = st.text_input("요약이 필요한 Youtube URL을 입력해주세요.")

if url:
    # response = requests.post("http://localhost:8080/summary", json={"url": url})
    # video_id = response.json()["video_id"]

    
    st.video(url
    
    # st.error("Invalid YouTube URL")