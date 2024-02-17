from rq import Queue
from src.module.infrastructure.message_queue.redis_connection import (
    get_redis_connection,
)


def get_task_queue():
    redis_conn = get_redis_connection()
    return Queue(connection=redis_conn)
