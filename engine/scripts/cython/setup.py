from setuptools import setup, Extension
from Cython.Build import cythonize

import sysconfig

path = "engine/scripts/cython/"

from setuptools import setup

ext_modules = [
    Extension(
        "engine.scripts.cython.build.test",
        [f"{path}test.pyx"]
    )
]

setup(
    ext_modules=cythonize(ext_modules)
)

# py -3.13t engine/scripts/cython/setup.py build_ext --inplace

""" setup(
    name="arak.test",
    ext_modules=cythonize(
        f"{path}test.pyx",
        compiler_directives={"language_level":"3"}
    )
) """
