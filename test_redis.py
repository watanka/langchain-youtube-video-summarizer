from backend.background_job import SaveDataJob
import fakeredis
import json
import pytest

@pytest.fixture
def fake_redis() :
    return fakeredis.FakeStrictRedis()

def test_save_and_get_job(fake_redis) : 
    job = SaveDataJob(job_id = '123', src_url = 'test.com')

    fake_redis.set(job.job_id, job.json())

    retrieved_job = fake_redis.get(job.job_id)
    
    retrieved_job = SaveDataJob.parse_raw(retrieved_job.decode('utf-8'))
    assert retrieved_job.job_id == job.job_id
    assert retrieved_job.src_url == job.src_url

    # change value in job description

    


