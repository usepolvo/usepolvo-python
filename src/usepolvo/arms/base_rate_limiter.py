# usepolvo/arms/base_rate_limiter.py

import time
from abc import ABC, abstractmethod
from collections import deque
from functools import wraps
from threading import Lock
from typing import Any, Callable, Dict


class BaseRateLimiter(ABC):
    def __init__(self):
        self.windows: Dict[str, deque] = {}
        self.lock = Lock()

    @abstractmethod
    def wait_if_needed(self, *args, **kwargs):
        """
        Check if a request can be made based on the rate limits.
        If not, wait until it's allowed.
        """
        pass

    def _clean_old_requests(self, window_name: str, current_time: float, time_frame: float):
        """
        Remove old requests from the specified window.

        :param window_name: The name of the window to clean
        :param current_time: The current timestamp
        :param time_frame: The time frame for the window (in seconds)
        """
        cutoff = current_time - time_frame
        while self.windows[window_name] and self.windows[window_name][0] <= cutoff:
            self.windows[window_name].popleft()

    def _wait_if_window_full(self, window_name: str, limit: int, time_frame: float) -> float:
        """
        Wait if the specified window is full.

        :param window_name: The name of the window to check
        :param limit: The maximum number of requests allowed in the window
        :param time_frame: The time frame for the window (in seconds)
        :return: The current time after waiting (if necessary)
        """
        current_time = time.time()
        self._clean_old_requests(window_name, current_time, time_frame)

        if len(self.windows[window_name]) >= limit:
            sleep_time = time_frame - (current_time - self.windows[window_name][0])
            if sleep_time > 0:
                time.sleep(sleep_time)
            current_time = time.time()
            self._clean_old_requests(window_name, current_time, time_frame)

        self.windows[window_name].append(current_time)
        return current_time

    def _initialize_window(self, window_name: str):
        """
        Initialize a new window if it doesn't exist.

        :param window_name: The name of the window to initialize
        """
        if window_name not in self.windows:
            self.windows[window_name] = deque()

    @abstractmethod
    def get_limits(self) -> Dict[str, Any]:
        """
        Get the current rate limits for the API.
        This method should be implemented by subclasses to return
        the specific rate limits for each API.

        :return: A dictionary containing the rate limits
        """
        pass

    @classmethod
    def rate_limited(cls, func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "rate_limiter") or not isinstance(self.rate_limiter, BaseRateLimiter):
                raise AttributeError("The class must have a 'rate_limiter' attribute of type BaseRateLimiter")
            self.rate_limiter.wait_if_needed()
            return func(self, *args, **kwargs)

        return wrapper
