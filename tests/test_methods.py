import unittest
from flask  import Flask, abort, request, make_response, current_app , Response
from flatapi import *
from flatapi.methods import *
import flatapi
import requests
import json
from pprint import pprint as pp
import os
from flata import *


class TestMethods(unittest.TestCase):
    def setUp(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        cfg_file = os.path.join(this_dir, 'test.config.json')

        app = Flask(__name__)
        self.api = FlatApi(app, cfg_file = cfg_file)
        self.db = Flata(self.api.db_file)
        self.app = app

    def tearDown(self):
        self.db.close()

        if os.path.exists(self.api.db_file):
            os.remove(self.api.db_file)

    def test_server_api(self):
        endpoint = server_api('','', '','', None )

        pp(endpoint.__name__)
        pp(type(endpoint))
        assert endpoint is not None 
        assert callable(endpoint)
        assert endpoint.__name__ =='restapi'

 
    def test_output_json_status_code(self):

        with self.app.test_request_context('/'):
            rep = output_json({}, 200)
            assert rep.status_code  == 200


    def test_output_json_data(self):
        with self.app.test_request_context('/'):
            rep = output_json(dict(data='data'), 200)
            assert rep.data  == b'{"data": "data"}\n'

    def test_get_not_exists(self):
        with self.app.test_request_context('/'):
            kwargs = {}
            kwargs[CONFIG_DB] = self.api.db_file
            kwargs[CONFIG_STORAGE] = FILE_STORAGE
            kwargs[RESOURCE_DOCUMENT] = 'not_exists'
            pp(kwargs)
            rep = get(**kwargs)
            assert rep.status_code  == 200
            assert rep.data  == b'[]\n'

    def test_post(self):       
        self.db.purge_tables()

        with self.app.test_request_context('/'):
            kwargs = {}
            kwargs[CONFIG_DB] = self.api.db_file
            kwargs[CONFIG_STORAGE] = FILE_STORAGE
            kwargs[RESOURCE_DOCUMENT] = 'posts'
            kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'
            rep = post(**kwargs)
            assert rep.status_code  == 201
            self.assertEqual( json.loads(rep.data.decode()) , 
                {"id": 1, "text": "post 1", "author": "harry" } )      

    def test_put(self):       
        self.db.purge_tables()

        with self.app.test_request_context('/'):
            kwargs = {}
            kwargs[CONFIG_DB] = self.api.db_file
            kwargs[CONFIG_STORAGE] = FILE_STORAGE
            kwargs[RESOURCE_DOCUMENT] = 'posts'
            kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'
            rep = post(**kwargs)
            assert rep.status_code  == 201

            kwargs[RESOURCE_DATA] = b'{\"text\": \"post updated\", \"author\": \"john\" }'
            kwargs[RESOURCE_QUERY] = {}
            kwargs[RESOURCE_QUERY][RESOURCE_ID] = 1

            rep = put(**kwargs)

            self.assertEqual( json.loads(rep.data.decode())[0] ,
                {'id':1, 'text': 'post updated', 'author': 'john'})


    def test_delete(self):       
        self.db.purge_tables()

        with self.app.test_request_context('/'):
            kwargs = {}
            kwargs[CONFIG_DB] = self.api.db_file
            kwargs[CONFIG_STORAGE] = FILE_STORAGE
            kwargs[RESOURCE_DOCUMENT] = 'posts'
            kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'
            rep = post(**kwargs)
            assert rep.status_code  == 201

            # kwargs[RESOURCE_DATA] = b'{\"text\": \"post updated\", \"author\": \"john\" }'
            kwargs[RESOURCE_QUERY] = {}
            kwargs[RESOURCE_QUERY][RESOURCE_ID] = 1

            rep = delete(**kwargs)

            assert rep.status_code == 200
            self.assertEqual( json.loads(rep.data.decode())[0] , [1])

    def test_get(self):  
        self.db.purge_tables()

        with self.app.test_request_context('/'):
            kwargs = {}
            kwargs[CONFIG_DB] = self.api.db_file
            kwargs[CONFIG_STORAGE] = FILE_STORAGE
            kwargs[RESOURCE_DOCUMENT] = 'posts'
            kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'
            rep = post(**kwargs)
            assert rep.status_code  == 201
            self.assertEqual( json.loads(rep.data.decode()) , 
                {"id": 1, "text": "post 1", "author": "harry" } )          

            rep = get(**kwargs)
            assert rep.status_code  == 200
            self.assertEqual( json.loads(rep.data.decode()) , 
                [{"id": 1, "text": "post 1", "author": "harry" }] )

if __name__ == "__main__":
    unittest.main()            