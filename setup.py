import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="kimi",
    version="0.1",
    author="Anjana Vakil",
    author_email="anjanavakil@gmail.com",
    description="A toy programming language that keeps it minimal",
    license="MIT",
    url="https://github.com/vakila/kimi",
    install_requires=[],
    packages=['samples', 'kimi'],
    scripts=['kimi/kimi'],
    long_description=read('README.md'),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft",
        "Operating System :: Microsoft :: MS-DOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        ""
    ],
)