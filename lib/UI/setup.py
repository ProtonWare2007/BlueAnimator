from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("./lib/UI/UIColorSelectorC.pyx", compiler_directives={'language_level': "3"}))

