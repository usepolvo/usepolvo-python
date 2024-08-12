# usepolvo/tentacles/salesforce/rate_limiter.py

from usepolvo.arms.base_rate_limiter import BaseRateLimiter


class SalesforceRateLimiter(BaseRateLimiter):
    def __init__(self):
        super().__init__()
        self.requests_per_day = 100000  # Adjust based on your Salesforce edition
        self._initialize_window("day")

    def wait_if_needed(self):
        with self.lock:
            self._wait_if_window_full("day", self.requests_per_day, 86400)  # 24 hours in seconds

    def get_limits(self):
        return {"requests_per_day": self.requests_per_day}
