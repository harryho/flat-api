# coding=utf-8
from setuptools import setup, find_packages
from codecs import open
import os


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return open(path, encoding='utf-8').read()

requirements = [
    'Flask>=0.8',
    'pseudb>=3.0.0'
]

setup(
    name="pseuserver",
    version="2.1.0",
    packages=find_packages(),

    # development metadata
    zip_safe=True,

    # metadata for upload to PyPI
    author="Harry Ho",
    author_email="harry.ho_long@yahoo.com",
    description="is a zero-coding restful API server inspired by Json-Server and Eve" 
                ". It is designed to be used as fake restful api for development, "
                " especially for people want to stick with Python stack. Setup process "
                " is less than 1 minute. ",
    license="MIT",
    keywords="web server json restful fake api",
    url="https://github.com/harryho/pseu-server",
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
    install_requires=requirements,
    long_description=read('README.rst'),
)
