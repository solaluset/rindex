import os
import sys

from Cython.Build import cythonize
from setuptools import Extension, setup


enable_exts = os.getenv("ENABLE_RINDEX_EXTENSIONS")
if not enable_exts:
    enable_exts = sys.implementation.name != "pypy"
else:
    try:
        enable_exts = bool(("0", "1").index(enable_exts))
    except ValueError:
        raise ValueError("ENABLE_RINDEX_EXTENSIONS: must be 0, 1 or empty") from None

setup(
    ext_modules=cythonize(
        [
            Extension(
                "rindex.c_rindex",
                sources=["rindex/c_rindex.pyx"],
                language="c",
            )
        ],
        language_level=3,
    )
    if enable_exts
    else None,
)
