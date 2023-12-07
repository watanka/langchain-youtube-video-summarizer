import logging
from logging import Formatter, getLogger, StreamHandler
from concurrent.futures import ProcessPoolExecutor
import asyncio
import os
from time import sleep

from langserve import RemoteRunnable
import httpx
from src.backend import store_data_job
from src.backend.configurations import ServiceConfigurations, CacheConfigurations
from dotenv import load_dotenv

load_dotenv()




log_format = Formatter("[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d]  %(message)s",
                       datefmt='%d/%b/%Y:%H:%M:%S (%Z)'
                       )
logger = getLogger('monitor')
stdout_handler = StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)

# fileConfig('logging.conf')
# logger = logging.getLogger('endpoint')



transcriber_service_url = ServiceConfigurations.services.get('transcriber', 'http://transcriber:5000') + '/transcribe/'
summarizer_service_url = ServiceConfigurations.services.get('summarizer', 'http://summarizer:6000') + '/summarize/'

mapreduce_chain = RemoteRunnable(summarizer_service_url)


logger.debug(f'transcriber service url : {transcriber_service_url}')
logger.debug(f'summarizer service url : {summarizer_service_url}')
summary_dir = str(os.getenv('SUMMARY_PATH', 'summaries'))
logger.debug(f'summary will be stored in : {summary_dir}')

def _trigger_prediction_if_queue(transcriber_url : str, summarizer_service_url : str) :
    job_id = store_data_job.right_pop_queue(CacheConfigurations.queue_name)
    if job_id is not None :

        url = store_data_job.get_data_redis(job_id)
        logger.debug(f'pop a job [{job_id}] to process from redis queue')

        # call transcriber endpoint
        try :
            transcriber_response = httpx.post(transcriber_url,
                    headers = {'Content-Type' : 'application/json'},
                    params = {'url' : url, 'job_id' : job_id},
                    timeout = None)
        except : # 
            logger.debug(f'error occurs at transcription api.')

        logger.debug(f'job_id[{job_id}] has been sent to [transcriber].')
        transcription_json = transcriber_response.json()
        
        transcription_path = transcription_json['transcription_path']
        video_id = transcription_json['video_id']

        logger.debug(f'job_id[{job_id}] received response from [transcriber].')


        summary_path = f'{summary_dir}/{video_id}_summary.txt'

        
        logger.debug(f'job_id[{job_id}] has been sent to [summarizer].')
        
        try :
            summary_response = httpx.post(summarizer_service_url,
                                            headers = {'Content-Type' : 'application/json'},
                                            params = {'job_id' : job_id,
                                                    'transcript_path' : str(transcription_path),
                                                    'summary_path' : str(summary_path)
                                                    },
                                            timeout = None
                                            )
        except :
            logger.debug(f'error occurs at summary api.')

        logger.debug(f'job_id[{job_id}] received response from [summarizer]')
        logger.debug(f'job_id[{job_id}][summarizer response] : {summary_response["summary"]}')

        summary = summary_response.json()['summary']
        store_data_job.set_data_redis(job_id, summary)

        




def _loop() :
    # send job request to transcriber & summarizer
    while True :
        sleep(1)
        _trigger_prediction_if_queue(transcriber_service_url, summarizer_service_url)
    


def monitoring_loop(num_procs : int = 4) :
    executor = ProcessPoolExecutor(num_procs)
    loop = asyncio.get_event_loop()

    for _ in range(num_procs) :
        asyncio.ensure_future(loop.run_in_executor(executor, _loop))

    loop.run_forever()

def main() :
    NUM_PROCS = int(os.getenv('NUM_PROCS', 1))
    logger.debug(f'monitoring runs {NUM_PROCS} processes.')
    monitoring_loop(NUM_PROCS)

if __name__ == '__main__' :
    logger.info('start monitoring')
    main()