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




