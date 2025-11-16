from app.tasks.base import BaseTask

class FibonacciTask(BaseTask):
    def execute(self, input_data: dict) -> dict:
        n = input_data["n"]
        if not isinstance(n, int) or n < 0 or n > 100:
            raise ValueError("'n' must be integer 0-100")
        
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
         
        return {"result": a}