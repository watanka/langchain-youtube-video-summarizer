from logging import DEBUG, Formatter, StreamHandler, getLogger
from concurrent.futures import ProcessPoolExecutor
import asyncio
import os
from time import sleep

import httpx
import store_data_job
from configurations import ServiceConfigurations, CacheConfigurations



log_format = Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
logger = getLogger('monitor')
stdout_handler = StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(DEBUG)


transcriber_service_url = ServiceConfigurations.services.get('transcriber', 'http://transcriber:5000') + '/transcribe/'
summarizer_service_url = ServiceConfigurations.services.get('summarizser', 'http://summarizer:6000') + '/summarize/'
logger.debug(f'transcriber service url : {transcriber_service_url}')
logger.debug(f'summarizer service url : {summarizer_service_url}')


def _trigger_prediction_if_queue(transcriber_url : str, summarizer_service_url : str) :
    job_id = store_data_job.right_pop_queue(CacheConfigurations.queue_name)

    if job_id is not None : # found job to proces
        url = store_data_job.get_data_redis(job_id)
        if url != '' :
            return True

        transcriber_response = httpx.post(transcriber_url,
                   headers = {'Content-Type' : 'application/json'},
                   params = {'url' : url},
                   timeout = None)
        logger.debug('request has been sent to [transcriber].')
        transcription_path = transcriber_response.json()['transcription_path']
        logger.debug('received response from [transcriber].')
        # 중간값 우선 redis에 등록


        summarize_response = httpx.post(summarizer_service_url,
                                        headers = {'Content-Type' : 'application/json'},
                                        params = {'transcript_path' : str(transcription_path)},
                                        timeout = None
                                        )
        logger.debug('request has been sent to [summarizer].')
        summary_content = summarize_response.json()['summary']
        logger.debug('received response from [summarizer]')
        # 값 redis에 등록
        # TODO 만약 prediction이 아무런 값도 나오지 않거나, 의미없는 값일 때, 다시 큐에 집어넣음
        logger.debug(f'set job_id : {job_id} with summary.\n summary : {summary_content}')
        store_data_job.set_data_redis(job_id, summary_content)

        




def _loop() :
    # send job request to transcriber & summarizer

    while True :
        sleep(1)
        _trigger_prediction_if_queue(transcriber_service_url, summarizer_service_url)
    


def monitoring_loop(num_procs : int = 2) :
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