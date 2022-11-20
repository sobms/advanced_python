from setuptools import setup, Extension

setup(
    name="cutils",
    version="1.0",
    description="C extension for matrix multiplication",
    author="Sobolev Mikhail",
    ext_modules=[Extension("cutils", ["cutils.cpp"])],
)
