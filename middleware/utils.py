import functools

def decorator(f):
    """
    Create a traditional decorator
    from a flattened(uncurried) interface.
    """
    @functools.wraps(f)
    def decorator_wrapper(g):
        @functools.wraps(g)
        def wrapper(*args, **kwargs):
            return f(g, *args, **kwargs)
        return wrapper
    return decorator_wrapper


@decorator
def log_call(call_next, *args, **kwargs):
    """Decorator to log the call signature"""
    arg_items = [str(a) for a in args] + [
    	f"{k}={v}" for k,v in kwargs.items()
    ]
    arg_string = ",".join(arg_items)
    print(f"Calling {call_next}({arg_string})")
    return call_next(*args, **kwargs)





