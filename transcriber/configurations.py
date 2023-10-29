import os
from logging import getLogger

logger = getLogger(__name__)

class CacheConfigurations :
    cache_host = os.getenv('CACHE_HOST', 'redis')
    cache_port = int(os.getenv('CACHE_PORT', 6379))
    queue_name = os.getenv('QUEUE_NAME', 'queue')

class RedisCacheConfigurations(CacheConfigurations) :
    redis_db = int(os.getenv('REDIS_DB', 0))
    redis_decode_responses = bool(os.getenv('REDIS_DECODE_RESPONSES', True))

logger.info(f'{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}')