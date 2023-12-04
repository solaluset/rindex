from sys import maxsize


def rindex(seq, value, start=0, stop=maxsize, /):
    size = len(seq)

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

    i = stop - 1
    while i >= start:
        if seq[i] == value:
            return i
        i -= 1

    raise ValueError("sequence.index(x): x not in sequence")
