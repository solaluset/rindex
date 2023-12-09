import sys
import json
import os.path
from random import shuffle
from time import perf_counter
from argparse import ArgumentParser

from test_rindex import FUNCTIONS


TEST_TIME = 1
MIN_COUNT = 10
WARMUP_COUNT = 5
STEPS = 10
SIZES = (100, 10_000, 1_000_000)


def test(func, args):
    # warm-up
    for _ in range(WARMUP_COUNT):
        try:
            func(*args)
        except Exception:
            pass

    total_time = 0
    count = 0
    while total_time < TEST_TIME or count < MIN_COUNT:
        t = perf_counter()
        try:
            func(*args)
        except:  # bare except is faster
            pass
        total_time += perf_counter() - t
        count += 1

    return total_time * 1000 / count


def _numbers_for(size):
    numbers = [-1]
    numbers.extend(range(0, size, size // STEPS))
    if numbers[-1] != size - 1:
        numbers.append(size - 1)
    return tuple(numbers)


def _get_name(func):
    try:
        file = func.__code__.co_filename
    except AttributeError:
        return func.__qualname__
    return os.path.splitext(os.path.basename(file))[0] + "." + func.__qualname__


def rindex_alternative1(seq, value):
    return len(seq) - 1 - seq[::-1].index(value)


def rindex_alternative2(seq, value):
    seq.reverse()
    try:
        return len(seq) - 1 - seq.index(value)
    finally:
        seq.reverse()


def rindex_alternative3(seq, value):
    for i, elem in enumerate(reversed(seq)):
        if elem == value:
            return len(seq) - 1 - i
    raise ValueError("value not in sequence")


FUNCTIONS = (
    (list.index,)
    + FUNCTIONS
    + (rindex_alternative1, rindex_alternative2, rindex_alternative3)
)


def test_list_size(func, size):
    assert size % STEPS == 0, f"can't divide the size into {STEPS} equal parts"
    list_ = list(range(size))
    # randomize the list to avoid possible optimizations
    shuffle(list_)
    numbers = _numbers_for(size)
    if func is list.index:
        numbers = numbers[:1] + tuple(reversed(numbers[1:]))
    return [test(func, (list_, list_[i] if i != -1 else size)) for i in numbers]


def run_measurements():
    results = []
    axis = _numbers_for(100)
    for size in SIZES:
        print("List size:", size)
        lines = []

        for func in FUNCTIONS:
            fname = _get_name(func)
            print("Function:", fname)

            values = test_list_size(func, size)
            if len(values) < len(axis):
                values.append(values[-1])
            lines.append((fname, values))
        results.append((size, lines))

    return results


def write_plots(results):
    import mpld3
    import matplotlib.pyplot as plt

    axis = _numbers_for(100)
    f = open("plots.html", "w")
    f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')

    for size, plot in results:
        plt.title(f"list of {size} elements")
        plt.xlabel("position")
        plt.ylabel("milliseconds")
        for fname, values in plot:
            plt.plot(axis, values, label=fname)
        plt.legend()
        f.write(mpld3.fig_to_html(plt.gcf()))
        plt.clf()

    f.close()


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("--json", action="store_true")
    p.add_argument("--from-json", action="store_true")
    p.add_argument("--append", action="store_true")

    args = p.parse_args(sys.argv[1:])

    if args.from_json or args.append:
        with open("results.json") as f:
            plots = json.load(f)
    else:
        plots = []

    if not args.from_json:
        plots.extend(run_measurements())

    if args.json:
        with open("results.json", "w") as f:
            json.dump(plots, f)
    else:
        write_plots(plots)
