import redis
from typing import Optional
from app.config import REDIS_URL

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


def push_task(task_id: int, priority: int = 3):
    if not 1 <= priority <= 5:
        raise ValueError("Priority must be 1-5")

    redis_client.lpush(priority, task_id)


def pop_task(timeout: int = 3) -> Optional[int]:
    queues = [5, 4, 3, 2, 1]

    result = redis_client.brpop(queues, timeout=timeout)

    if result:
        queue_name, task_id = result
        return int(task_id)

    return None
