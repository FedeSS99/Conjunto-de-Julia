from numpy.lib.utils import get_include
from setuptools import setup, Extension
from Cython.Build import cythonize

modulo_externo = [Extension(
    "RutinasJulia",
    ["RutinasJulia.pyx"],
    extra_compile_args = ["/openmp"],
    extra_link_args = ["/openmp"]
)]

setup(
    ext_modules=cythonize(modulo_externo, annotate=True),
    include_dirs=[get_include()],
    zip_safe=False
)
