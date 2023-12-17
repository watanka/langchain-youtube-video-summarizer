import streamlit as st
import pandas as pd

import requests
import httpx
import asyncio
import os
import logging


logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s')
proxy_port = os.getenv('PROXY_PORT', '8080')
summary_path = os.getenv('SUMMARY_PATH', 'summaries')


st.title('Langchain Summarizer:sunglasses:')


async def send_httpx(method, url, params = None) :
    if method == 'get' :
        httpx_func = httpx.AsyncClient.get
    elif method == 'post' :
        httpx_func = httpx.AsyncClient.post

    response = await httpx_func(url, params)
    return response.json()


async def request_summary(url : str) :
    return asyncio.run(send_httpx('post', f'http://proxy:{proxy_port}/summary', json = {'url' : url}))
    
async def query_summary_result(job_id : str) :
    return asyncio.run(send_httpx('get', f'http://proxy:{proxy_port}/jobs/{job_id}'))

async def fetch_summary_result_async() :
    async with httpx.AsyncClient() as client :
        response = await client.get(f'http://proxy:{proxy_port}/jobs/{job_id}')
        return response.json()
    return asyncio.run(fetch_summary_result_async())

@st.cache_data
def list_all_result() :
    all_summaries = requests.get(f'http://proxy:{proxy_port}/allsummaries').json()
    return all_summaries

# col1, col2 = st.columns(2)

# with col1 :
#     st.text('인풋의 형태를 골라주세요👉')

# with col2 : 
#     st.selectbox(label='input type', options = ['Youtube URL',])

# input_form, submit_button = st.columns(2)

with st.form('my_form') :
    # with input_form :
    url = st.text_input("요약이 필요한 Youtube URL을 입력해주세요.", key = 'url')
    # with submit_button :
    submitted = st.form_submit_button('summarize!')
    if submitted :
        response = requests.post(f"http://proxy:{proxy_port}/summary", json={"url": url})
        job_id = response.text
        st.session_state.job_id = job_id
        st.text(f'당신의 요청이 {st.session_state.job_id}로 등록되었습니다.')    
        st.video(url)

if 'job_id' in st.session_state.keys() :
    st.write(st.session_state.job_id)
else :
    st.write('job id is not defined')

for i, result in enumerate(list_all_result()) :
    with open(result['summary_path'], 'r') as f : 
        summary_result = f.read()
    st.text_area(f'요약 결과{i}', summary_result, height = 300)

    


if st.button('결과 확인!') :
    # data = query_summary_result(st.session_state.job_id)

    query_by_jobid_response = requests.get(f'http://proxy:{proxy_port}/jobs/{st.session_state["job_id"]}')
    
    logging.debug(f'query by jobid response : {query_by_jobid_response.json()}')
    # job_id_summary = query_by_jobid_response.json()[st.session_state['job_id']]
    st.write(f'요약 : \n{query_by_jobid_response.json()}') # {job_id_summary}')

        
    # st.error("Invalid YouTube URL")