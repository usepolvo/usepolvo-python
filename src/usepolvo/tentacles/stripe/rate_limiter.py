import time
from collections import deque
from threading import Lock


class StripeRateLimiter:
    def __init__(self, read_limit: int = 100, write_limit: int = 100):
        self.read_limit = read_limit
        self.write_limit = write_limit
        self.read_window = deque()
        self.write_window = deque()
        self.lock = Lock()

    def _clean_old_requests(self, current_time: float, window: deque, limit: int) -> None:
        cutoff = current_time - 1  # 1 second window
        while window and window[0] <= cutoff:
            window.popleft()

    def wait_if_needed(self, is_write_operation: bool = False) -> None:
        with self.lock:
            current_time = time.time()
            if is_write_operation:
                self._clean_old_requests(current_time, self.write_window, self.write_limit)
                if len(self.write_window) >= self.write_limit:
                    sleep_time = 1 - (current_time - self.write_window[0])
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    current_time = time.time()
                    self._clean_old_requests(current_time, self.write_window, self.write_limit)
                self.write_window.append(current_time)
            else:
                self._clean_old_requests(current_time, self.read_window, self.read_limit)
                if len(self.read_window) >= self.read_limit:
                    sleep_time = 1 - (current_time - self.read_window[0])
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    current_time = time.time()
                    self._clean_old_requests(current_time, self.read_window, self.read_limit)
                self.read_window.append(current_time)
