import unittest
from flask  import Flask
import pseuserver
from pseuserver import *
import requests
import json
from pprint import pprint as pp
try:
    from mock import Mock
except:
    # python3
    from unittest.mock import Mock
import os


class TestApi(unittest.TestCase):
    def setUp(self):
        pass

    def test_default_init(self):
        server = PseuServer()
        assert server.app is None
        assert server.prefix is ''
        assert len(server.routes) == 0

    def test_init_without_config(self):
        with self.assertRaises(Exception) as context:
            server = PseuServer(Mock(), prefix='', cfg_file='')
            self.assertTrue('The config.json is not found.' in context.exception)

    def test_init_empty_config(self):        
        with self.assertRaises(Exception) as context:
            self.this_dir = os.path.dirname(os.path.realpath(__file__))
            self.cfg_file = os.path.join(self.this_dir, 'test.empty.config.json')
            server = PseuServer(Mock(), prefix='', cfg_file=self.cfg_file)
            self.assertTrue('The config.json is not found.' in context.exception)

    def test_init_simple_config(self):
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file = os.path.join(self.this_dir, 'test.simple.config.json')
        
        server = PseuServer(Flask(__name__), prefix ='', cfg_file = self.cfg_file)
        assert server.app is not None
        assert server.prefix == pseuserver.DEFAULT_API_PREFIX
        assert server.db == pseuserver.DEFAULT_DB
        assert len(server.urls) == 0
        assert len(server.routes) == 0 

    def test_init_advanced_config(self):
        # pseuserver.DEFAULT_CONFIG = 'test.advanced.config.json'

        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.cfg_file = os.path.join(self.this_dir, 'test.advanced.config.json')

        server = PseuServer(Flask(__name__), prefix='/api', cfg_file = self.cfg_file)
        assert server.app is not None
        assert server.prefix == '/api'
        assert server.db == 'test.advanced.db.json'
        assert len(server.urls) == 2
        assert len(server.routes) == 8
        assert server.routes ==  ['/api/posts', '/api/posts/', '/api/posts/<int:id>', 
            '/api/posts/<int:id>/<string:embed>', '/api/comments', '/api/comments/', 
            '/api/comments/<int:id>', '/api/comments/<int:id>/<string:embed>'] 


if __name__ == "__main__":
    unittest.main()