from concurrent.futures import ThreadPoolExecutor
import json
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Task, TaskStatus
from app.redis_client import pop_task
from app.tasks.registry import TASK_REGISTRY

logger = logging.getLogger(__name__)


def process_task(task_id: int, db: Session):
    task = db.get(Task, task_id)
    
    if task is None:
        logger.warning(f"Task with ID {task_id} not found.")
        return
    
    if task.status != TaskStatus.PENDING:
        logger.warning(f"Task {task_id} already processed (status: {task.status.value})")
        return

    if task.task_type not in TASK_REGISTRY:
        task.status = TaskStatus.FAILED
        task.result = f"Unknown task type: {task.task_type}"
        db.commit() 
        return

    task.status = TaskStatus.RUNNING
    db.commit()
    
    try:
        executor = TASK_REGISTRY[task.task_type]()
        input_data = json.loads(task.input_data) if task.input_data else {}
        
        result = executor.execute(input_data)
        
        task.result = json.dumps(result)
        task.status = TaskStatus.COMPLETED
        db.commit()

        result_data = json.loads(task.result)
        logger.info(f"Task {task_id} COMPLETED - Result: {result_data}")
        
    
    except Exception as e:
        task.result = str(e)
        task.status = TaskStatus.FAILED
        db.commit()
        logger.error(f"Task {task_id} FAILED: {str(e)}")



def run_worker():
    logger.info("Worker started. Waiting for tasks...")
    
    while True:
        task_id = pop_task(timeout=3)
        
        if task_id is None:
            continue
        
        logger.info(f"Processing task {task_id}...")
        
        db = SessionLocal()
        try:
            process_task(task_id, db)
        finally:
            db.close()


def run_worker_pool(num_workers: int = 3):
    logger.info(f"Starting worker pool with {num_workers} threads...")
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(run_worker) for _ in range(num_workers)]
        
        try:
            for future in futures:
                future.result()
        except KeyboardInterrupt:
            logger.info("Shutting down worker pool...")

if __name__ == "__main__":
    run_worker()