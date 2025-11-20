import sys
from app.database import SessionLocal
from app.models import Task
from tabulate import tabulate


def show_tasks(limit):
    db = SessionLocal()
    tasks = db.query(Task).order_by(Task.id.desc()).limit(limit).all()
    
    if not tasks:
        print("No tasks in database")
        db.close()
        return
    
    data = []
    for task in tasks:
        data.append([
            task.id,
            task.task_type,
            task.status.value,
            task.priority,
            task.input_data[:40] + "..." if task.input_data and len(task.input_data) > 40 else (task.input_data or ""),
            task.result[:40] + "..." if task.result and len(task.result) > 40 else (task.result or "")
        ])
    
    print(f"\nShowing last {len(tasks)} tasks:\n")
    print(tabulate(data, headers=["ID", "Type", "Status", "Priority", "Input", "Result"], tablefmt="grid"))
    
    db.close()


def clear_tasks(limit):
    db = SessionLocal()
    
    total = db.query(Task).count()
    to_delete = min(limit, total)
    
    if to_delete == 0:
        print("No tasks to delete")
        db.close()
        return
    
    tasks_to_delete = db.query(Task).order_by(Task.id).limit(to_delete).all()
    
    for task in tasks_to_delete:
        db.delete(task)
    
    db.commit()
    print(f"Deleted {to_delete} tasks from database")
    
    db.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Commands:")
        print("- python manage_db.py show <n>")
        print("- python manage_db.py clear <n>")
        sys.exit(1)
    
    command = sys.argv[1]
    num = int(sys.argv[2])
    
    if command == "show":
        show_tasks(num)
    elif command == "clear":
        clear_tasks(num)
    else:
        print(f"\nUnknown command: {command}")
        print("Use 'show' or 'clear'\n")