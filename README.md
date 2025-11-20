# Task Queue API

A case study of distributed task queue system using priority-based processing.

## Stack

- FastAPI - REST API
- PostgreSQL - task metadata and results storage
- Redis - priority queue broker
- SQLAlchemy - ORM
- Docker - containerized PostgreSQL and Redis

## System Overview

1. POST request to API creates a task record in PostgreSQL
2. Task ID is pushed to the appropriate Redis queue based on priority (1=lowest, 5=highest)
3. Workers check Redis queues from highest to lowest priority (5 -> 1) using BRPOP
4. Worker updates task status: PENDING -> RUNNING -> COMPLETED/FAILED
5. Results are stored back in PostgreSQL

## Setup

### 1. Start infrastructure
```bash
docker-compose up -d
```
### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Initialize database
```bash
python init_db.py
```
## Running the System

### Terminal 1 - API
```bash
uvicorn app.main:app --reload
```
API available at http://localhost:8000

### Terminal 2 - Worker
```bash
python -m app.worker
```
Run multiple workers in separate terminals to process tasks simultaneously.

## Usage

### Create a task
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "FibonacciTask",
    "input_data": {"n": 10},
    "priority": 4
  }'
```
Response:
```json
{
  "id": 1,
  "task_type": "FibonacciTask",
  "status": "pending",
  "priority": 4,
  "created_at": "1970-01-01T00:00:00"
}
```
### Check task status
```bash
curl http://localhost:8000/tasks/1
```
Response after processing:
```json
{
  "id": 1,
  "task_type": "FibonacciTask",
  "status": "completed",
  "result": "{\"result\": 55}",
  "priority": 4
}
```
## Demo & Utilities

### Demo Tool
```bash
python demo.py --tasks 500 --workers 10
```

### Database Commands
```bash
python manage_db.py show 10
python manage_db.py clear 100
```
