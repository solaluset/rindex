import sys

from rindex.rindex import rindex
from rindex.pypy_rindex import rindex as pypy_rindex

FUNCTIONS = (rindex, pypy_rindex)
try:
    from rindex.c_rindex import rindex as c_rindex
except ImportError:
    if sys.implementation.name != "pypy":
        raise
else:
    FUNCTIONS += (c_rindex,)

import pytest


TEST_LIST = [0, 1, 0, 2, 0]


def all_functions(f):
    return pytest.mark.parametrize("func", FUNCTIONS)(
        pytest.mark.parametrize("li", [TEST_LIST])(f)
    )


class BadInt(int):
    def __eq__(self, _):
        raise RuntimeError("go away")


class BizarreObject:
    def __eq__(self, _):
        return False


@all_functions
def test_basic(func, li):
    li_copy = li.copy()

    assert func(li, 0) == 4
    assert li == li_copy
    assert func(li, 1) == 1

    with pytest.raises(ValueError):
        func(li, -1)
    assert li == li_copy


@all_functions
def test_not_list(func, li):
    assert func(tuple(li), 2) == 3


@all_functions
def test_start(func, li):
    assert func(li, 0, -10) == 4

    li = li.copy()
    li[1] = BadInt(li[1])

    assert func(li, 0, 0, 1) == 0
    assert func(li, 0, -3) == 4
    with pytest.raises(RuntimeError):
        func(li, -1, 1)
    with pytest.raises(ValueError):
        func(li, -1, 2)


@all_functions
def test_stop(func, li):
    assert func(li, 0, 0, 4) == 2
    assert func(li, 0, 0, -1) == 2
    assert func(li, 0, 0, -3) == 0

    li = [BadInt(x) for x in li]

    with pytest.raises(ValueError):
        func(li, 0, 0, -5)
    with pytest.raises(ValueError):
        func(li, 0, 0, -40)


def test_exceptions():
    exceptions = set()
    for f in FUNCTIONS:
        with pytest.raises(ValueError) as ctx:
            f([], 0)
        exceptions.add(ctx.value.args)
    assert len(exceptions) == 1


@all_functions
def test_same_object(func, li):
    b = BizarreObject()
    # this must work with rindex if it works in the built-in index
    [b].index(b)
    func([b], b)
