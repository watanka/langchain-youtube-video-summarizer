from fastapi import FastAPI, BackgroundTasks
import httpx

import logging
import asyncio

import os
import json
from typing import Dict, Any


from tools import convert_video2audio
from schemas import UserRequest
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
def request_summary(user_request : UserRequest, background_tasks : BackgroundTasks) :
    logger.debug('transcriber_service_url', transcriber_service_url)
    transcriber_response = httpx.post(transcriber_service_url +'/transcribe/', 
                                        headers = {'Content-Type' : 'application/json'}, 
                                        params = {"url" : user_request.url}, 
                                        timeout = None)
    transcription_path = transcriber_response.json()['transcription_path']
    # # 3. summarize from llm server
    logger.debug('transcription_path', transcription_path)
    summarize_response = httpx.post(summarizer_service_url + '/summarize/', 
                                    headers = {'Content-Type' : 'application/json'}, 
                                    params = {'transcript_path' : str(transcription_path)}, 
                                    timeout = None)
    logger.debug('summarize_response', summarize_response)
    return summarize_response.json()['summary']