import operator as op
import functools
import re

TARGET_PATH_REGEX = re.compile(r"(\w+)(?:\.(\w+))?")

def split_path(path):
    host, port = re.match(TARGET_PATH_REGEX, path).groups()
    return host, port


class Forward:
    def __init__(self, processor=None, path=None, cached=True):
        self.processor = processor
        self.host, self.port = split_path(path)
        self.targetter = op.attrgetter(path) if self.host and self.port else None
        self.cached = cached

    def __set_name__(self, type, name):
        if self.port is None:
            self.port = name
        self.targetter = op.attrgetter(f"{self.host}.{self.port}")

    def __get__(self, owner, type):
        if owner is None:
            return self
        else:
            if self.cached and self.port in vars(owner):
                return getattr(owner, port)
            if self.processor is None:
                attr = self.targetter(owner)
            else:
                attr = self.processor(self.targetter(owner))
            if self.cached:
                setattr(owner, self.port, attr)
            return attr


if __name__ == "__main__":
    from middleware.utils import log_call
    class middleware:
        def __init__(self, target):
            self.target = target
    
        get = Forward(log_call, "target")

