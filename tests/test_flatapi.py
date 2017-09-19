import unittest
from flask  import Flask
import flatapi
from flatapi import *
import requests
import json
# from pprint import pprint as pp
try:
    from mock import Mock
except:
    # python3
    from unittest.mock import Mock
import os
import pytest

class TestApi(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_init(self):
        server = FlatApi()
        assert server.app is None
        assert server.prefix is ''
        assert len(server.routes) == 0

    @pytest.mark.skipif(sys.version_info < (2, 7),
                    reason="requires python2.7+")
    def test_init_without_config(self):
        with self.assertRaises(Exception) as context:
            server = FlatApi(Mock())
            self.assertTrue('The config.json is not found.' in context.exception)

    @pytest.mark.skipif(sys.version_info < (2, 7),
                        reason="requires python2.7+")
    def test_init_empty_config(self):       
        with self.assertRaises(Exception) as context:
            self.this_dir = os.path.dirname(os.path.realpath(__file__))
            self.cfg_file = os.path.join(self.this_dir, 'test.empty.config.json')
            server = FlatApi(Mock(), cfg_file=self.cfg_file, prefix='')
            self.assertTrue('The config.json is not found.' in context.exception)

    def test_init_simple_config(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file = os.path.join(self.this_dir, 'test.simple.config.json')
        
        server = FlatApi(Flask(__name__), cfg_file = self.cfg_file)
        assert server.app is not None
        assert server.prefix == flatapi.DEFAULT_API_PREFIX
        assert server.db == flatapi.DEFAULT_DB
        assert len(server.urls) == 0
        assert len(server.routes) == 0 

    def test_init_no_config(self):
        # self.this_dir = os.path.dirname(os.path.realpath(__file__))
        # self.cfg_file = os.path.join(self.this_dir, 'test.simple.config.json')
        
        server = FlatApi(Flask(__name__), cfg_file = '', storage='MEMORY', no_cfg=True)
        assert server.app is not None
        assert server.prefix == flatapi.DEFAULT_API_PREFIX
        assert server.db == flatapi.DEFAULT_DB
        assert len(server.urls) == 0
        assert len(server.routes) == 3 
    def test_init_momery_config(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file = os.path.join(self.this_dir, 'test.memory.config.json')

        server = FlatApi(Flask(__name__), cfg_file = self.cfg_file, prefix='')
        assert server.app is not None
        assert server.db == 'db.json'
        assert server.storage == MEMORY_STORAGE
        assert len(server.urls) == 2
        assert len(server.routes) == 8
        assert isinstance(server.cache, (CachingMiddleware, MemoryStorage))
        
    def test_init_cache_momery_config(self):
        server = FlatApi(Flask(__name__), cfg_file = '' , prefix='', storage='MEMORY')
        assert server.app is not None
        assert server.db == 'db.json'
        assert server.storage == MEMORY_STORAGE
        assert len(server.urls) == 0
        assert len(server.routes) == 0
        assert isinstance(server.cache, (CachingMiddleware, MemoryStorage))

    def test_init_advanced_config(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file = os.path.join(self.this_dir, 'test.advanced.config.json')

        server = FlatApi(Flask(__name__), cfg_file = self.cfg_file, prefix='/api')
        assert server.app is not None
        assert server.prefix == '/api'
        assert server.db == 'test.advanced.db.json'
        assert len(server.urls) == 2
        assert len(server.routes) == 8
        assert server.routes ==  ['/api/posts', '/api/posts/', '/api/posts/<int:id>', 
            '/api/posts/<int:id>/<string:embed>', '/api/comments', '/api/comments/', 
            '/api/comments/<int:id>', '/api/comments/<int:id>/<string:embed>'] 


    def test_load_config(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file = os.path.join(self.this_dir, 'test.simple.config.json')
        
        server = FlatApi(Flask(__name__), cfg_file = self.cfg_file)
        assert server.app is not None
        assert server.prefix == flatapi.DEFAULT_API_PREFIX
        assert server.db == flatapi.DEFAULT_DB
        assert len(server.urls) == 0
        assert len(server.routes) == 0 

        server.config_file = os.path.join(self.this_dir, 'test.advanced.config.json')
        server.load_config()
        assert server.prefix == '/api'
        assert server.db == 'test.advanced.db.json'
        assert len(server.urls) == 2
        assert len(server.routes) == 0


    def test_add_routes(self):

        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file = os.path.join(self.this_dir, 'test.simple.config.json')
        
        server = FlatApi(Flask(__name__), cfg_file = self.cfg_file)


        server.config_file = os.path.join(self.this_dir, 'test.advanced.config.json')
        server.load_config()

        assert server.prefix == '/api'
        assert server.db == 'test.advanced.db.json'
        assert len(server.urls) == 2
        assert len(server.routes) == 0

        server.add_routes()
        assert len(server.routes) == 8
        assert server.routes ==  ['/api/posts', '/api/posts/', '/api/posts/<int:id>', 
            '/api/posts/<int:id>/<string:embed>', '/api/comments', '/api/comments/', 
            '/api/comments/<int:id>', '/api/comments/<int:id>/<string:embed>'] 


    def test_complete_routes(self):        
        server = FlatApi()
        routes = server.complete_routes('/test_url')

        assert routes ==  ['/test_url', '/test_url/', '/test_url/<int:id>', 
            '/test_url/<int:id>/<string:embed>'] 

if __name__ == "__main__":
    unittest.main()