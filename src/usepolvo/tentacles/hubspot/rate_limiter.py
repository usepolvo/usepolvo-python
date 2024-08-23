from usepolvo.arms.base_rate_limiter import BaseRateLimiter


class HubSpotRateLimiter(BaseRateLimiter):
    def __init__(self, limit: int = 100):
        super().__init__()
        self.limit = limit
        self._initialize_window("api")

    def wait_if_needed(self):
        with self.lock:
            self._wait_if_window_full("api", self.limit, 10)  # 10 second window

    def get_limits(self):
        return {"api_limit": self.limit}
