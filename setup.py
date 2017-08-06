# coding=utf-8
from setuptools import setup, find_packages
from codecs import open
import os


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path, encoding='utf-8').read()


setup(
    name="pseuserver",
    version="1.0.0.RC1",
    packages=find_packages(),

    # development metadata
    zip_safe=True,

    # metadata for upload to PyPI
    author="Harry Ho",
    author_email="harry.ho_long@yahoo.com",
    description="is a Zero-Coding restful API server inspired by Json-Server_ and Eve_" 
                ". It is designed to be used as fake restful api for development, "
                " especially for people want to use Python stack.",
    license="MIT",
    keywords="database json nosql",
    url="https://github.com/harryho/pseuserver",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Topic :: Restful API",
        "Topic :: Restful API :: Fake API",
        "Topic :: Json Server",
        "Topic :: Zero Coding",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent"
    ],

    long_description=read('README.rst'),
)
