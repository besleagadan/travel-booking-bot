import time
from functools import wraps

def retry(times=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt+1} failed: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator
