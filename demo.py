import argparse
import random
import time
import requests
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:8000"

TASK_CONFIGS = {
    "FibonacciTask": [0, 100],
    "CountPrimes": [1_000_000, 5_000_000],
    "CollatzTask": [1, 10_000_000]
}

session = requests.Session()

def create_task():
    task_type = random.choice(list(TASK_CONFIGS.keys()))
    min_val, max_val = TASK_CONFIGS[task_type]
    
    payload = {
        "task_type": task_type,
        "input_data": {"n": random.randint(min_val, max_val)},
        "priority": random.randint(1, 5)
    }
    
    r = session.post(f"{BASE_URL}/tasks/", json=payload)
    r.raise_for_status()
    return r.json()["id"]

def get_status(task_id):
    r = session.get(f"{BASE_URL}/tasks/{task_id}")
    r.raise_for_status()
    return r.json()["status"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", type=int, default=500)
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()
    
    processes = []

    if args.workers > 0:
        print(f"Starting {args.workers} worker processes...")
        for _ in range(args.workers):
            p = subprocess.Popen([sys.executable, "-m", "app.worker"])
            processes.append(p)
        time.sleep(2)
    
    print(f"Creating {args.tasks} tasks...")
    with ThreadPoolExecutor(max_workers=50) as pool:
        task_ids = list(pool.map(lambda _: create_task(), range(args.tasks)))
    
    print(f"Created {len(task_ids)} tasks\n")
    start_time = time.time()
    
    while True:
        with ThreadPoolExecutor(max_workers=50) as pool:
            statuses = list(pool.map(get_status, task_ids))
        
        pending = statuses.count("pending")
        completed = statuses.count("completed")
        failed = statuses.count("failed")
        
        print(f"PENDING: {pending:4d} | COMPLETED: {completed:4d} | FAILED: {failed:4d}")
        
        if pending == 0:
            break
        
        time.sleep(2)
    
    elapsed = time.time() - start_time
    
    print(f"\nCompleted: {completed} | Failed: {failed}")
    print(f"Total time: {elapsed:.1f}s")
    print(f"Average per task: {(elapsed / args.tasks) * 1000:.1f}ms")
    
    if processes:
        print("\nTerminating worker processes...")
        for p in processes:
            p.terminate()
            p.wait(timeout=5)
    
    session.close()