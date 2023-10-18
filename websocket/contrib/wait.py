import signal


def timeout(seconds):
    def decorator(function):
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise Exception(f"Timeout of {function.__name__} function")
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            result = function(*args, **kwargs)
            signal.alarm(0)
            return result
        return wrapper
    return decorator
