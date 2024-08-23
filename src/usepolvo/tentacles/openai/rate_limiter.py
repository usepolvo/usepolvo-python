from usepolvo.arms.base_rate_limiter import BaseRateLimiter


class OpenAIRateLimiter(BaseRateLimiter):
    def __init__(self, limit: int = 60):
        super().__init__()
        self.limit = limit
        self._initialize_window("requests")

    def wait_if_needed(self):
        with self.lock:
            self._wait_if_window_full("requests", self.limit, 60)  # 60 second window

    def get_limits(self):
        return {"requests_per_minute": self.limit}
