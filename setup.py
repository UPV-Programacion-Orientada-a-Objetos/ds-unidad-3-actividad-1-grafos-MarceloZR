from setuptools import setup,Extension
from Cython.Build import cythonize
import os
cpp=os.path.join(os.path.dirname(__file__),'cpp')
ext=[Extension('py.graph_wrapper',
    sources=['py/graph_wrapper.pyx',os.path.join(cpp,'GrafoDisperso.cpp')],
    include_dirs=[cpp],language='c++',extra_compile_args=['-std=c++17','-O2'])]
setup(name='neuronet',ext_modules=cythonize(ext,language_level='3'),packages=['py'])
