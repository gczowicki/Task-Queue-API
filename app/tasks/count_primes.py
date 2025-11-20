from app.tasks.base import BaseTask

class CountPrimes(BaseTask):
    def execute(self, input_data: dict) -> dict:
        n = input_data["n"]
        if not isinstance(n, int) or n < 0 or n > 5_000_000:
            raise ValueError("'n' must be integer 0 - 5*10^6")

        if n < 2:
            return {"result": 0}

        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False

        for i in range(2, int(n ** 0.5) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False

        return {"result": sum(sieve)}