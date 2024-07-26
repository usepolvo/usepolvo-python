from ratelimit import limits, sleep_and_retry
from retry import retry

# Stripe's rate limit: 100 requests per second (adjust as needed)
CALLS = 100
PERIOD = 1  # 1 second


@sleep_and_retry
@limits(calls=CALLS, period=PERIOD)
@retry(tries=3, delay=2, backoff=2)
def rate_limited_call(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
