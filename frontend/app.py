import streamlit as st
import requests
import httpx
import asyncio
import os
import logging

logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s')
proxy_port = os.getenv('PROXY_PORT', '8080')

st.title('Langchain Summarizer:sunglasses:')


def fetch_summary_result(job_id : str) : 
    async def fetch_summary_result_async() :
        async with httpx.AsyncClient() as client :
            response = await client.get(f'http://proxy:{proxy_port}/jobs/{job_id}')
            return response.json()
    return asyncio.run(fetch_summary_result_async())

col1, col2 = st.columns(2)

with col1 :
    st.text('인풋의 형태를 골라주세요👉')

with col2 : 
    st.selectbox(label='input type', options = ['Youtube URL',])

url = st.text_input("요약이 필요한 Youtube URL을 입력해주세요.")

if url:
    response = requests.post(f"http://proxy:{proxy_port}/summary", json={"url": url})
    job_id = response.text
    st.session_state['job_id'] = job_id
    st.text(f'당신의 요청이 {job_id}로 등록되었습니다.')
    
    st.video(url)
    
    if st.button('submit') :
        data = fetch_summary_result(job_id)
        summary = data[st.session_state['job_id']]['prediction']
        
        st.write(f'요약 : \n{summary}')

        
    # st.error("Invalid YouTube URL")