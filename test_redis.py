from src.backend.background_job import SaveDataJob
import fakeredis
import json
import pytest

@pytest.fixture
def fake_redis() :
    return fakeredis.FakeStrictRedis()


def left_push_queue(redis_client, queue_name: str, key : str) -> bool :
    try : 
        redis_client.lpush(queue_name, key)
        return True
    except Exception :
        return False
    
def right_pop_queue(redis_client, queue_name: str) :
    if redis_client.llen(queue_name) > 0 :
        return redis_client.rpop(queue_name)
    else : 
        return None

def list_jobs_in_queue(redis_client, queue_name : str) : 
    return redis_client.lrange(queue_name, 0, -1)


def test_save_and_get_job(fake_redis) : 
    job = SaveDataJob(job_id = '123', src_url = 'test.com')

    fake_redis.set(job.job_id, job.json())

    retrieved_job = fake_redis.get(job.job_id)
    
    retrieved_job = SaveDataJob.parse_raw(retrieved_job.decode('utf-8'))
    assert retrieved_job.job_id == job.job_id
    assert retrieved_job.src_url == job.src_url


def test_lpush_and_rpop(fake_redis) :
    job = SaveDataJob(job_id = '123', src_url = 'test.com')

    left_push_queue(fake_redis, queue_name = 'test-queue', key = job.job_id)

    assert list_jobs_in_queue(fake_redis, queue_name='test-queue') == [job.job_id.encode('utf-8')]

    right_pop_queue(fake_redis, queue_name = 'test-queue') == job.job_id.encode('utf-8')
    


