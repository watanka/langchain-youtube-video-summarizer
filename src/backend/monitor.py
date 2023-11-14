from logging import DEBUG, Formatter, StreamHandler, getLogger
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




log_format = Formatter("[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d]  %(message)s")
logger = getLogger('monitor')
stdout_handler = StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(DEBUG)


transcriber_service_url = ServiceConfigurations.services.get('transcriber', 'http://transcriber:5000') + '/transcribe/'
summarizer_service_url = ServiceConfigurations.services.get('summarizer', 'http://summarizer:6000') + '/summarize/'

mapreduce_chain = RemoteRunnable(summarizer_service_url)


logger.debug(f'transcriber service url : {transcriber_service_url}')
logger.debug(f'summarizer service url : {summarizer_service_url}')


def _trigger_prediction_if_queue(transcriber_url : str, summarizer_service_url : str) :
    job_id = store_data_job.right_pop_queue(CacheConfigurations.queue_name)
    if job_id is not None : # found job to proces

        url = store_data_job.get_data_redis(job_id)
        logger.debug(f'job id : {job_id}')

        # call transcriber endpoint
        transcriber_response = httpx.post(transcriber_url,
                   headers = {'Content-Type' : 'application/json'},
                   params = {'url' : url, 'job_id' : job_id},
                   timeout = None)
        logger.debug('request has been sent to [transcriber].')
        transcription_json = transcriber_response.json()
        
        transcription_path = transcription_json['transcription_path']
        video_id = transcription_json['video_id']

        logger.debug('received response from [transcriber].')
        # 중간값 우선 redis에 등록


        summary_dir = str(os.getenv('SUMMARY_PATH', 'summaries'))
        summary_path = f'{summary_dir}/{video_id}_summary.txt'

        logger.debug(f'summarizer[input]\njob_id : {job_id}\ntranscription_path : {transcription_path}\nsummary_path : {summary_path}\n')
        logger.debug('request has been sent to [summarizer].')
        
        summary_response = httpx.post(summarizer_service_url,
                                        headers = {'Content-Type' : 'application/json'},
                                        params = {'job_id' : job_id,
                                                  'transcript_path' : str(transcription_path),
                                                  'summary_path' : str(summary_path)
                                                  },
                                        timeout = None
                                        )

        # read transcription as convert input ready for mapreduce chain.
        # with open(transcription_path, 'r') as f :
        #     transcription = f.read()
        # docs = text_split.split_docs(transcription)
        # logger.debug(f'input type for summarizer : [{type(docs)}]')
        # docs = [
        #     Document(
        #         page_content = split,
        #         metadata = None, # TODO add info from pytube
        #     ) for split in transcription.split('\n\n')
        # ]
        # summary_response = mapreduce_chain.invoke(docs, config = {'max_concurrency' : 6})
        # summary_content = summary_response
        logger.debug('received response from [summarizer]')
        logger.debug(f'[summarizer response] : {summary_response}')

        summary = summary_response.json()['summary']
        # summary_content = summarize_response.json()['summary']
        # logger.debug(f'summary response : {summary_content}')
        # logger.debug(f'set job_id : {job_id} with summary.\n')
        # # 값 redis에 등록
        # TODO 만약 prediction이 아무런 값도 나오지 않거나, 의미없는 값일 때, 다시 큐에 집어넣음
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
    NUM_PROCS = int(os.getenv('NUM_PROCS', 2))
    monitoring_loop(NUM_PROCS)

if __name__ == '__main__' :
    logger.info('start monitoring')
    main()