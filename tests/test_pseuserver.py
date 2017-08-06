import unittest
from flask  import Flask
import pseuserver
from pseuserver import *
import requests
import json
from pprint import pprint as pp
# import pseuserver
import os


class TestApi(unittest.TestCase):
    def setUp(self):
        pseuserver.DEFAULT_CONFIG = 'test.config.json'
        pseuserver.DEFAULT_DB = 'test.db.json'
        self.this_dir = os.path.dirname(os.path.realpath(__file__))

        self.cfg_file = os.path.join(self.this_dir, pseuserver.DEFAULT_CONFIG)


    def test_default_app(self):
        server = PseuServer()
        assert server.app is None
        assert server.prefix is ''
        assert len(server.routes) == 0

    def test_app_init(self):
        # pseuserver.DEFAULT_CONFIG = 'test.config.json'
        # this_dir = os.path.dirname(os.path.realpath(__file__))
        # cfg_file = os.path.join(this_dir, pseuserver.DEFAULT_CONFIG)

        server = PseuServer(Flask(__name__), prefix ='', cfg_file = self.cfg_file)
        assert server.app is not None
        assert server.prefix is ''
        assert len(server.urls) == 2
        assert len(server.routes) == 8
        assert server.routes ==  ['/posts', '/posts/', '/posts/<int:id>', 
            '/posts/<int:id>/<string:embed>', '/comments', '/comments/', 
            '/comments/<int:id>', '/comments/<int:id>/<string:embed>'] 
        # assert server.db  == DEFAULT_DB     

    def test_app_init_prefix(self):
        server = PseuServer(Flask(__name__), prefix='/api', cfg_file = self.cfg_file)
        assert server.app is not None
        assert server.prefix is '/api'
        assert len(server.urls) == 2
        assert len(server.routes) == 8
        assert server.routes ==  ['/api/posts', '/api/posts/', '/api/posts/<int:id>', 
            '/api/posts/<int:id>/<string:embed>', '/api/comments', '/api/comments/', 
            '/api/comments/<int:id>', '/api/comments/<int:id>/<string:embed>'] 


# def test_load_routes():
#     server = PseuServer(Flask(__name__), prefix='/api')
#     assert server.app is not None
#     assert server.prefix is '/api'
#     assert len(server.urls) == 2
#     assert len(server.routes) == 8
#     assert server.routes ==  ['/api/posts', '/api/posts/', '/api/posts/<int:id>', 
#         '/api/posts/<int:id>/<string:embed>', '/api/comments', '/api/comments/', 
#         '/api/comments/<int:id>', '/api/comments/<int:id>/<string:embed>'] 



if __name__ == "__main__":
    unittest.main()