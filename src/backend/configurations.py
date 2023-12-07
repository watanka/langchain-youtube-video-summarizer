import os
from typing import Dict
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('endpoint')



class ServiceConfigurations :
    services : Dict[str, str] = {}
    for environ in os.environ.keys() :
        if environ.endswith("_SERVICE") :
            url = f"http://{os.getenv(environ)}"
            services[environ.lower().replace('_service', '')] = url


class CacheConfigurations :
    cache_host = os.getenv('CACHE_HOST', 'redis')
    cache_port = int(os.getenv('CACHE_PORT', 6379))
    queue_name = os.getenv('QUEUE_NAME', 'redis_queue')

class RedisCacheConfigurations(CacheConfigurations) :
    redis_db = int(os.getenv('REDIS_DB', 0))
    redis_decode_responses = bool(os.getenv('REDIS_DECODE_RESPONSES', True))

logger.info(f'{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}')
logger.info(f'{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}')