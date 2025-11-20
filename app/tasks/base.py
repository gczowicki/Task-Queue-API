from abc import ABC, abstractmethod


class BaseTask(ABC):
    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        pass

    @classmethod
    def get_task_name(cls) -> str:
        return cls.__name__
