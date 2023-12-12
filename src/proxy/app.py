from fastapi import FastAPI, BackgroundTasks, Request, Depends
import httpx

from uuid import uuid4



from src.backend import background_job, store_data_job
from src.log_db import unit_of_work, db_setup

import logging
import asyncio

from sqlalchemy.orm import Session

from typing import Dict, Any
from src.proxy.schemas import UserRequest
from src.proxy.configurations import ServiceConfigurations


#logging
# logging.basicConfig(level=logging.DEBUG)

# fileConfig('logging.conf')
# logger = logging.getLogger('endpoint')
logging.basicConfig(level = logging.DEBUG, format = '[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s')

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
    logging.debug(f'received request with url : {user_request.url}')
    background_job.save_data_job(src_url=user_request.url,
                                 job_id = job_id,
                                 background_tasks = background_tasks,
                                 enqueue = True
                                 )

    return job_id


@app.get('/jobs/{job_id}')
async def summary_result(job_id: str, db : Session = Depends(db_setup.get_db)) -> str:

    uow = unit_of_work.SqlAlchemyUnitOfWork(db)

    with uow :
        mapreduce_info = uow.mapreduce_repo.get(job_id)

    with open(mapreduce_info.summary_path, 'r') as f :
        summary_str = f.read()

    # result = {job_id : {'prediction' : ''}}
    # summary = store_data_job.get_data_redis(key = job_id)
    # result[job_id]['prediction'] = summary

    return summary_str

@app.get('/jobs')
def list_result() :
    return store_data_job.list_kv()