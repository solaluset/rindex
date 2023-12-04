from operator import indexOf
from itertools import islice


def rindex(seq, value, start=0, stop=None, /):
    size = len(seq)

    if stop is None:
        if start == 0:
            # shortcut common case
            return size - 1 - indexOf(reversed(seq), value)
        stop = 0
    else:
        stop = -stop if stop < 0 else size - stop

    return (
        size
        - 1
        - indexOf(
            islice(reversed(seq), stop, -start if start < 0 else size - start), value
        )
        - stop
    )
