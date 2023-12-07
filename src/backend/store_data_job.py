from logging import getLogger
# from logging.config import fileConfig
from src.backend.configurations import RedisCacheConfigurations
import redis
from typing import Any

# fileConfig('logging.conf')
# logger = getLogger('endpoint')

redis_client = redis.Redis(
    host = RedisCacheConfigurations.cache_host,
    port = RedisCacheConfigurations.cache_port,
    db = RedisCacheConfigurations.redis_db,
    decode_responses = RedisCacheConfigurations.redis_decode_responses
)


def left_push_queue(queue_name: str, key : str) -> bool :
    try : 
        redis_client.lpush(queue_name, key)
        return True
    except Exception :
        return False
    
def right_pop_queue(queue_name: str) -> Any :
    if redis_client.llen(queue_name) > 0 :
        return redis_client.rpop(queue_name)
    else : 
        return None
    
def set_data_redis(key: str, value: str) -> bool :
    redis_client.set(key, value)
    return True

def get_data_redis(key: str) -> Any :
    data = redis_client.get(key)
    return data


def list_jobs_in_queue(queue_name : str) : 
    return redis_client.lrange(queue_name, 0, -1)

def list_kv() :
    keys = redis_client.keys('*')
    return {key : redis_client.get(key) for key in keys}