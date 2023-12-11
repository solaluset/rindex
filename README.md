# rindex

This package provides `rindex()` function that returns last index of value in sequence.

## Installing

```bash
pip install rindex
```

## Examples

```python
from rindex import rindex


numbers = [5, 1, 3, 8, 10, 5, 8, 1, 8, 3]

print(rindex(numbers, 1))  # 7

print(rindex(numbers, 8, 4, 8))  # 6
```

## Goals

- Support all features of built-in `.index()`

- Speed

- Portability (support for different platforms)

## Supported platforms

Currently, the library includes three `rindex()` implementations:

- Cython

- Pure Python (when the Cython one is not available; slower)

- Pure Python for PyPy

## Features

- Supports any sequences

- Supports `start` and `stop` (both may be negative or out of bounds)

- Doesn't copy the sequence

## Controlling Cython extensions

You can set environment variable `ENABLE_RINDEX_EXTENSIONS` to `0` or `1` to forcefully disable/enable Cython extensions.
This can be useful if you face compilation problems and want to use pure Python version.

## Benchmarking

`tests/benchmark.py` can generate interactive plots with comparisons of different implementations.
