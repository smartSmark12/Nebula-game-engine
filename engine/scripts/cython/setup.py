from setuptools import setup, Extension
from Cython.Build import cythonize

# warning:
# Windows needs .pyd files, Linux needs .so files !
# .pyx files are universal between both OSs
#
# command:
# py -3.13t engine/scripts/cython/setup.py build_ext --inplace
#
# this rudimentary system will get improved when the engine-wide auto-compilation comes up

# this is the file name you have to change to your own
NAME = "raycaster"

# you can change this to your own export path of the final pyd / so file
export_path = "engine.scripts.raycast"#"engine.scripts.cython.build"

# this you probably shouldn't touch
source_path = "engine/scripts/raycast/" #"engine/scripts/cython/"
file_extension = ".pyx"

ext_modules = [
    Extension(
        f"{export_path}.{NAME}",
        [f"{source_path}{NAME}{file_extension}"]
    )
]

setup(
    ext_modules=cythonize(ext_modules)
)
