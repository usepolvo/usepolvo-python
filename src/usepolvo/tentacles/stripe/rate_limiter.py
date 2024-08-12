# usepolvo/tentacles/stripe/rate_limiter.py

from usepolvo.arms.base_rate_limiter import BaseRateLimiter


class StripeRateLimiter(BaseRateLimiter):
    def __init__(self, read_limit: int = 100, write_limit: int = 100):
        super().__init__()
        self.read_limit = read_limit
        self.write_limit = write_limit
        self._initialize_window("read")
        self._initialize_window("write")

    def wait_if_needed(self, is_write_operation: bool = False):
        with self.lock:
            if is_write_operation:
                self._wait_if_window_full("write", self.write_limit, 1)  # 1 second window
            else:
                self._wait_if_window_full("read", self.read_limit, 1)  # 1 second window

    def get_limits(self):
        return {"read_limit": self.read_limit, "write_limit": self.write_limit}
