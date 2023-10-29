import os
from logging import getLogger
from typing import Dict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = getLogger(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY', '')


class ServiceConfigurations :
    services : Dict[str, str] = {}
    for environ in os.environ.keys() :
        if environ.endswith("_SERVICE") :
            url = f"http://{os.getenv(environ)}"
            services[environ.lower().replace('_service', '')] = url


class CacheConfigurations :
    cache_host = os.getenv('CACHE_HOST', 'redis')
    cache_port = int(os.getenv('CACHE_PORT', 6379))
    queue_name = os.getenv('QUEUE_NAME', 'queue')

class RedisCacheConfigurations(CacheConfigurations) :
    redis_db = int(os.getenv('REDIS_DB', 0))
    redis_decode_responses = bool(os.getenv('REDIS_DECODE_RESPONSES', True))

logger.info(f'{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}')