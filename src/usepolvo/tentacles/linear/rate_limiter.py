# usepolvo/tentacles/linear/rate_limiter.py

from usepolvo.arms.base_rate_limiter import BaseRateLimiter


class LinearRateLimiter(BaseRateLimiter):
    def __init__(self):
        super().__init__()
        self.requests_per_minute = 240
        self.requests_per_day = 14400
        self._initialize_window("minute")
        self._initialize_window("day")

    def wait_if_needed(self):
        with self.lock:
            current_time = self._wait_if_window_full("minute", self.requests_per_minute, 60)
            self._wait_if_window_full("day", self.requests_per_day, 86400)  # 24 hours in seconds

    def get_limits(self):
        return {"requests_per_minute": self.requests_per_minute, "requests_per_day": self.requests_per_day}
