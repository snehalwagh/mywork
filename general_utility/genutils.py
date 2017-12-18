#TODO make this a tuple and change code accordingly
#TODO create the globals.py and have const
#TODO http://code.activestate.com/recipes/65207-constants-in-python/?in=user-97991

#TODO No setting happens except in __init__ so use a const. --> init datamembers must be const. and methods should not change self.

#TODO create utils.py --> having const class and memoize decorator, etc/

#TODO add debug ipython lines here, to easily add into code. also make a decorator

import collections
import functools32
import typecheck

#TODO rename to memoize
memoized = functools32.lru_cache
accepts = typecheck.accepts
returns = typecheck.returns

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock',
    #'cache.regions': 'short_term, long_term',
    'cache.regions': 'short_term',
    'cache.short_term.type': 'ext:memcached',
    #'cache.short_term.type': 'memory',
    'cache.short_term.url': '127.0.0.1:11211',
    'cache.short_term.expire': '3600',
    #'cache.long_term.type': 'file',
    #'cache.long_term.expire': '86400',
}
cache = CacheManager(**parse_cache_config_options(cache_opts))

import warnings

def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.'''
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func

def find_shortest_path(graph, start, end, path=[]):
    """
    change this to a better implementation of dijkstra
    also move this to some tag_tree_utils file
    """
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

# Example usage
if __name__ == "__main__":
    # Will cache up to 100 items, dropping the least recently used if
    # the limit is exceeded.
    @memoized(100)
    @accepts(int)
    def fibo(n):
        if n > 1:
            return fibo(n - 1) + fibo(n - 2)
        else:
            return n

    def fibono(n):
        if n > 1:
            return fibono(n - 1) + fibono(n - 2)
        else:
            return n

    # Same as above, but with no limit on cache size
    @memoized
    def fibonl(n):
        if n > 1:
            return fibo(n - 1) + fibo(n - 2)
        else:
            return n

    print fibo(125)

