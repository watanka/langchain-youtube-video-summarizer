from logging import getLogger
from redis_client import redis_client
from typing import Any

logger = getLogger(__name__)

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



