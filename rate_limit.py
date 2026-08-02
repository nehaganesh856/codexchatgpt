from collections import defaultdict
import time


class SimpleRateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def is_allowed(self, key: str, limit: int = 100, period: int = 60) -> bool:
        now = time.time()

        self.requests[key] = [
            t for t in self.requests[key]
            if now - t < period
        ]

        if len(self.requests[key]) >= limit:
            return False

        self.requests[key].append(now)
        return True


limiter = SimpleRateLimiter()