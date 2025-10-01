# --- FILE: utils/decorators.py ---
import time
from functools import wraps

LOG_FILE = "function_log.txt"

def log_action(func):
    """Decorator 1: Logs function calls to a file."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        log_message = f"[LOG] Running {func.__name__} at {time.ctime()}\n"
        with open(LOG_FILE, "a") as f:
            f.write(log_message)
        return func(*args, **kwargs)
    return wrapper

def measure_time(func):
    """Decorator 2: Measures execution time and logs it to a file."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_message = f"[TIME] {func.__name__} executed in {end - start:.4f} sec\n"
        with open(LOG_FILE, "a") as f:
            f.write(time_message)
        return result
    return wrapper