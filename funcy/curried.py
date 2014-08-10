# Copied from Toolz (https://github.com/pytoolz/toolz) with modifications.

import inspect

from toolz import curry

import py2


def _nargs(f):
    try:
        return len(inspect.getargspec(f).args)
    except TypeError:
        return None


def do_curry(f):
    return callable(f) and _nargs(f)


d = {}
for name, f in py2.__dict__.items():
  if name in py2.__all__ and name != 'curry':
    if do_curry(f):
      f = curry(f)
    d.update({name: f})

d.update(dict(
  (f.__name__, curry(f)) for f in [map, filter, reduce]
))

locals().update(d)

