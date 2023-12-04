__all__ = ("rindex",)

import sys
from functools import wraps
from typing import Sequence, TypeVar


ElemT = TypeVar("ElemT")


def rindex(
    seq: Sequence[ElemT], value: ElemT, start: int = 0, stop: int = None, /
) -> int:
    """Returns last index of value in sequence.

    Raises ValueError if the value is not present.

    Optional `start` and `stop` arguments limit searching to `seq[start:stop]`."""

    ...


update_metadata = wraps(rindex)

if sys.implementation.name == "pypy":
    from .pypy_rindex import rindex
else:
    try:
        from .c_rindex import rindex
    except ImportError:
        from .rindex import rindex

# set annotations and docstring
update_metadata(rindex)
# remove unnecessary functions
del rindex.__wrapped__
del update_metadata
