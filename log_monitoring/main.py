import time
import click
import datetime
from log_monitoring import monitoring
from logging import DEBUG, Formatter, StreamHandler, getLogger


logger = getLogger(__name__)
logger.setLevel(DEBUG)
formatter = Formatter("[%(asctime)s] [%(levelname)s] [%(process)d] [%(name)s] [%(funcName)s] [%(lineno)d] %(message)s",
                       datefmt='%d/%b/%Y:%H:%M:%S (%Z)')

handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter,
                     )
logger.addHandler(handler)


@click.command('monitoring request/response')
@click.option('--interval', type = int, default = 1)
def monitor(interval) :

    while True :

        # pytube 정보 확인
        now = datetime.datetime.now()
        interval_ago = now - datetime.timedelta(minutes=(interval + 1))
        time_later = now.strftime("%Y-%m-%d %H:%M:%S")
        time_before = interval_ago.strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"time between {time_before} and {time_later}")
        invalid_requests = monitoring.invalid_request(time_before, time_later)
        complete_requests = monitoring.complete_request(time_before, time_later)
        
        logger.info(f'Invalid Request between {time_before} and {time_later} : {len(invalid_requests)}')
        logger.info(f'Complete Request between {time_before} and {time_later} : {len(complete_requests)}')

        # TODO transcription evaluation
        # TODO summarization evaluation 

        time.sleep(interval * 60)

        

if __name__ == '__main__' :
    monitor()