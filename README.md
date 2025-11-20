# Task Queue API

A distributed task-processing system built with the following main components: 1) REST API accepting task requests 2) priority queue broker 3) database storing task data 4) workers processing tasks asynchronously. This architecture is common in applications that need background processing like email services, webhook handling, or data exports.

## Stack

- FastAPI - REST API
- PostgreSQL - task metadata and results storage
- Redis - priority queue broker (5 priority levels)
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
source venv/bin/activate  # Windows: venv\Scripts\activate
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

curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "FibonacciTask",
    "input_data": {"n": 10},
    "priority": 4
  }'

Response:

{
  "id": 1,
  "task_type": "FibonacciTask",
  "status": "pending",
  "priority": 4,
  "created_at": "2024-01-15T10:30:00"
}

### Check task status

curl http://localhost:8000/tasks/1

Response after processing:

{
  "id": 1,
  "task_type": "FibonacciTask",
  "status": "completed",
  "result": "{\"result\": 55}",
  "priority": 4
}

## Demo & Utilities

### Demo Tool
```bash
python demo.py --tasks 500 --workers 3
```
Creates 500 random tasks, spawns 3 worker processes and displays real-time progress.

### Basic database management

View last N tasks:
python manage_db.py show 10

Clear first N tasks:
python manage_db.py clear 100