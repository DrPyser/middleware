"""
Implement a "Gateway", a wrapper object
that can intercept attribute access to the wrapped object
and apply transformations(e.g. decorators).

This can be used as an alternative to monkey patching,
by storing and managing decorated/patched attributes in a separate layer.
"""
import functools


class Gateway:
    __slots__ = ["__dict__", "_target", "_middlewares", "_cached"]
    def __init__(self, target, middlewares=(), cached=True):
        self._target = target
        self._middlewares = list(middlewares)
        self._cached = cached

    def _refresh_cache(self):
        if self._cached:
            attrs = vars(self).keys()
            self.__dict__.clear()
            for a in attrs:
                getattr(self, a)
                assert a in vars(self)
                
    def __getattr__(self, name):
        attr = functools.reduce(
            lambda acc, m: m(acc) (
            middleware
            for filter, middleware in self._middlewares
            if filter(name)
        ), getattr(self._target, name))
        if self._cached:
            setattr(self, name, attr)
        return attr


if __name__ == "__main__":
    from middleware.utils import log_call
    class test:
        def method1(self):
            return 1
    
        def method2(self):
            return 2
    
        def other(self):
            return 3
    
    import re
    g = Gateway(test(), middlewares=[
        (re.compile(r"method.").match, log_call)
    ])

    print(g.method1())
    print(g.method2())
    print(g.other())


