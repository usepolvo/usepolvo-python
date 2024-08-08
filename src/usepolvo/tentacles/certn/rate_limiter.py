# usepolvo/tentacles/certn/rate_limiter.py

import time
from collections import deque


class CertnRateLimiter:
    # ref: https://docs.certn.co/api/v/certn-api-v-1.0/faq#api-requests
    # 240 requests/minute (60s rolling window) and
    # 14,400 requests/day (24hr rolling window)

    def __init__(self):
        self.requests_per_minute = 240
        self.requests_per_day = 14400
        self.minute_window = deque()
        self.day_window = deque()

    def wait_if_needed(self):
        current_time = time.time()
        self._clean_old_requests(current_time)

        if len(self.minute_window) >= self.requests_per_minute or len(self.day_window) >= self.requests_per_day:
            oldest_allowed_minute = current_time - 60
            oldest_allowed_day = current_time - 86400  # 24 hours in seconds

            sleep_time = max(
                self.minute_window[0] - oldest_allowed_minute if self.minute_window else 0,
                self.day_window[0] - oldest_allowed_day if self.day_window else 0,
            )

            if sleep_time > 0:
                time.sleep(sleep_time)
                current_time = time.time()
                self._clean_old_requests(current_time)

        self.minute_window.append(current_time)
        self.day_window.append(current_time)

    def _clean_old_requests(self, current_time):
        minute_cutoff = current_time - 60
        day_cutoff = current_time - 86400

        while self.minute_window and self.minute_window[0] <= minute_cutoff:
            self.minute_window.popleft()

        while self.day_window and self.day_window[0] <= day_cutoff:
            self.day_window.popleft()
