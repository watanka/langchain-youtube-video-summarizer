from fastapi import FastAPI, BackgroundTasks
import httpx

from uuid import uuid4

import sys, os


from src.backend import background_job, store_data_job

import logging
import asyncio

import os
import json
from typing import Dict, Any
from src.proxy.schemas import UserRequest
from src.proxy.configurations import ServiceConfigurations

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


@app.post('/summary')
def request_summary(user_request : UserRequest, background_tasks : BackgroundTasks) :
    job_id = str(uuid4())[:6]

    background_job.save_data_job(src_url=user_request.url,
                                 job_id = job_id,
                                 background_tasks = background_tasks,
                                 enqueue = True
                                 )

    return job_id


@app.get('/jobs/{job_id}')
async def summary_result(job_id: str):
    result = {job_id : {'prediction' : ''}}
    summary = store_data_job.get_data_redis(key = job_id)
    result[job_id]['prediction'] = summary

    return result

@app.get('/jobs')
def list_result() :
    return store_data_job.list_kv()