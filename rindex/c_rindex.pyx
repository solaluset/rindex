from cython import Py_ssize_t

cdef extern from "Python.h":
    Py_ssize_t PY_SSIZE_T_MAX


def rindex(
    seq, value, start: Py_ssize_t = 0, stop: Py_ssize_t = PY_SSIZE_T_MAX, /
) -> Py_ssize_t:
    cdef Py_ssize_t size = len(seq)

    if start < 0:
        start += size
        if start < 0:
            start = 0

    if size < stop:
        stop = size
    elif stop < 0:
        stop += size
        if stop < 0:
            stop = 0

    cdef Py_ssize_t i
    for i in range(stop - 1, start - 1, -1):
        elem = seq[i]
        if elem is value or elem == value:
            return i

    raise ValueError("sequence.index(x): x not in sequence")
