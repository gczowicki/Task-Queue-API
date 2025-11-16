import app.tasks
from app.tasks.base import BaseTask

TASK_REGISTRY = {cls.get_task_name(): cls for cls in BaseTask.__subclasses__()}