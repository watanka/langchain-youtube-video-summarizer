from fastapi import FastAPI, BackgroundTasks
import httpx

import logging
import asyncio

import os
import json
from typing import Dict, Any


from tools import convert_video2audio
from schemas import SummaryRequest
from configurations import ServiceConfigurations

#logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

transcriber_service_url = ServiceConfigurations.services.get('transcriber', 'http://transcriber:5000')
summarizer_service_url = ServiceConfigurations.services.get('summarizer', 'http://summarizer:6000')

async def req(ac, service, url, api_endpoint) :
    response = await ac.get(f"{url}/{api_endpoint}")
    return service, response


@app.get('/health')
def health() -> Dict[str, str] :
    return {'health' : 'ok'}

@app.get('/health/all')
async def health_all() -> Dict[str, Any] :
    '''send healthcheck to all servers'''
    results = {}
    async with httpx.AsyncClient() as ac :
        tasks = [req(ac, service, url, 'health') for service, url in ServiceConfigurations.services.items()]

        responses = await asyncio.gather(*tasks)

        for service, response in responses : 
            results[service] = response.json()
    return results


@app.get('/list')
def list_summaries() :
    '''
    read all summaries in db.
    '''
    pass

@app.post('/summary')
def request_summary(summary_request : SummaryRequest, background_tasks : BackgroundTasks) :

    # 1. convert from video url to mp3
    audio_output_path = convert_video2audio(video_url = summary_request.url) # docker volume에 저장
    
    # 2. request to transriber server
    transcriber_service_url = 'http://transcriber:5000' + '/transcribe/'
    print('transriber url :', transcriber_service_url)
    logger.debug(audio_output_path)
    transcriber_response = httpx.post(transcriber_service_url, headers = {'Content-Type' : 'application/json'}, params = {"audiofile_path" : audio_output_path}, timeout = None)
    
    transcription_path = transcriber_response.json()['transcription_path']
    # # 3. summarize from llm server
    summarize_response = httpx.post(summarizer_service_url, headers = {'Content-Type' : 'application/json'}, json = {'trscript_path' : transcription_path}, timeout = None)

    return summarize_response.json()['summary']