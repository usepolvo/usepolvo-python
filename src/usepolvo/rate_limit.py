from functools import wraps

from ratelimit import limits, sleep_and_retry
from retry import retry


def rate_limited_call(calls, period):
    def decorator(func):
        @sleep_and_retry
        @limits(calls=calls, period=period)
        @retry(tries=3, delay=2, backoff=2)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
