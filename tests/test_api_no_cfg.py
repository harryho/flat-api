import unittest
from flask  import Flask
from flatapi import *
import flatapi
import requests
import json
# from pprint import pprint as pp
import os
from flata import *
from flata.middlewares import CachingMiddleware



class TestApiNoConfig(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        self.api = FlatApi(app, cfg_file = '', prefix='', storage=MEMORY_STORAGE)
        self.db = Flata(storage = self.api.cache)
        self.client = app.test_client()

    def tearDown(self):
        self.db.close()
        self.api.cache.close()


    def test_get_empty_result(self):
        response = self.client.get('/posts')

        data = response.data
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(json.loads(data.decode()), [])

    def test_get_no_data(self):
        response = self.client.get('/no_data')
        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 200)
        self.assertEqual(json.loads(data.decode()), [])

    def test_post(self):
        self.db.purge_tables()
        response = self.client.post('/posts', 
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 201)
        self.assertEqual(json.loads(data.decode()),
             {'id':1, 'text': 'post 1', 'author': 'harry'})

    def test_delete_all(self):
        self.db.purge_tables()
        response = self.client.post('/posts', 
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 201)
        assert len(json.loads(data.decode()))> 1

        response = self.client.delete('/posts')

        self.assertEqual(response.status_code, 200)

    def test_delete_by_id(self):
        self.db.purge_tables()
        response = self.client.post('/posts', 
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')


        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 201)
        assert len(json.loads(data.decode()))> 1  

        response=self.client.delete('/posts/1')
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        self.db.purge_tables()
        self.client.post('/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        response = self.client.put('/posts/1',
            data='{\"text\": \"post updated\", \"author\": \"john\" }')
        data =json.loads(response.data.decode())
        sc = response.status_code
        self.assertEqual(sc, 200)

        self.assertEqual(data[0],
             {'id':1, 'text': 'post updated', 'author': 'john'})

    def test_get_by_id(self):
        self.db.purge_tables()
        self.client.post('/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        response = self.client.get('/posts/1')

        data = response.data
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(json.loads(data.decode()),
             {'id':1, 'text': 'post 1', 'author': 'harry'})


    def test_get_by_query(self):
        self.db.purge_tables()
        self.client.post('/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        response = self.client.get('/posts?author=harry')

        data =json.loads(response.data.decode()) 
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(data[0],
             {'id':1, 'text': 'post 1', 'author': 'harry'})


    def test_get_by_id_with_embed(self):
        self.db.purge_tables()
        self.client.post('/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')
        self.client.post('/comments',
            data='{\"text\": \"comment 1\", \"commentator\": \"peter\", "postId": 1 }')

        response = self.client.get('/posts/1/comments')

        data =json.loads(response.data.decode()) 
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(data,
             {'id':1, 'text': 'post 1', 'author': 'harry',
                'comments': [{'commentator': 'peter',
               'id': 1,
               'postId': 1,
               'text': 'comment 1'}]
             })


    def test_get_by_id_with_expand(self):
        self.db.purge_tables()
        self.client.post('/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')
        self.client.post('/comments',
            data='{\"text\": \"comment 1\", \"commentator\": \"peter\", "postId": 1 }')

        response = self.client.get('/comments/1?expand=posts')

        data =json.loads(response.data.decode()) 
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(data,
             { 'commentator': 'peter', 'id': 1, 'postId': 1, 'text': 'comment 1',
               'post': {'id':1, 'text': 'post 1', 'author': 'harry'}
             })



if __name__ == "__main__":
    unittest.main()