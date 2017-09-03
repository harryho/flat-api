#!/usr/bin/env python

import functools

from nose import SkipTest
import pytest

from flata.middlewares import CachingMiddleware
from flata.storages import MemoryStorage
from flata import Flata

def expected_failure(test):
    @functools.wraps(test)
    def inner(*args, **kwargs):
        try:
            test(*args, **kwargs)
        except Exception:
            raise SkipTest
        else:
            raise AssertionError('Failure expected')
    return inner





# @pytest.fixture
# def db():
#     db_ = Flata('test.db.json', storage=MemoryStorage)
#     db_.purge_tables()
#     return db_


# @pytest.fixture
# def storage():
#     _storage = CachingMiddleware(MemoryStorage)
#     return _storage()  # Initialize MemoryStorage
