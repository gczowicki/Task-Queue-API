from app.tasks.base import BaseTask


class CollatzTask(BaseTask):
    def execute(self, input_data: dict) -> dict:
        n = input_data["n"]
        if not isinstance(n, int) or not 1 <= n <= 10_000_000:
            raise ValueError("'n' must be integer 1-10000000")

        steps = 0
        while n != 1:
            n = n // 2 if n % 2 == 0 else 3 * n + 1
            steps += 1

        return {"result": steps}
