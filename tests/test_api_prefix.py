import unittest
from flask  import Flask
from flatapi import *
import flatapi
import requests
import json
# from pprint import pprint as pp
import os
from flata import *



class TestApiWithPrefix(unittest.TestCase):
    def setUp(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        cfg_file = os.path.join(this_dir, 'test.config.json')

        app = Flask(__name__)
        self.api = FlatApi(app, cfg_file = cfg_file, prefix ='api')
        self.db = Flata(self.api.db_file)
        self.client = app.test_client()


    def tearDown(self):
        self.db.close()

        if os.path.exists(self.api.db_file):
            os.remove(self.api.db_file)


    def test_get_empty_result(self):
        response = self.client.get('/api/posts')

        data = response.data
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(json.loads(data.decode()), [])

    def test_get_404_error(self):
        response = self.client.get('/api/not_exist')
        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 404)

    def test_post(self):
        self.db.purge_tables()
        response = self.client.post('/api/posts', 
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 201)
        self.assertEqual(json.loads(data.decode()),
             {'id':1, 'text': 'post 1', 'author': 'harry'})

    def test_delete_all(self):
        self.db.purge_tables()
        response = self.client.post('/api/posts', 
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 201)
        assert len(json.loads(data.decode()))> 1  

        response = self.client.delete('/api/posts')

        self.assertEqual(response.status_code, 200)

    def test_delete_by_id(self):
        self.db.purge_tables()
        response = self.client.post('/api/posts', 
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        data = response.data
        sc = response.status_code
        # pp(response)
        self.assertEqual(sc, 201)
        assert len(json.loads(data.decode()))> 1   

        response=self.client.delete('/api/posts/1')
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        self.db.purge_tables()
        self.client.post('/api/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        response = self.client.put('/api/posts/1',
            data='{\"text\": \"post updated\", \"author\": \"john\" }')
        data =json.loads(response.data.decode())
        sc = response.status_code
        self.assertEqual(sc, 200)

        self.assertEqual(data[0],
             {'id':1, 'text': 'post updated', 'author': 'john'})

    def test_get_by_id(self):
        self.db.purge_tables()
        self.client.post('/api/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        response = self.client.get('/api/posts/1')

        data = response.data
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(json.loads(data.decode()),
             {'id':1, 'text': 'post 1', 'author': 'harry'})

    def test_get_by_id(self):
        self.db.purge_tables()
        self.client.post('/api/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        response = self.client.get('/api/posts/1')

        data = response.data
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(json.loads(data.decode()),
             {'id':1, 'text': 'post 1', 'author': 'harry'})

    def test_get_by_query(self):
        self.db.purge_tables()
        self.client.post('/api/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')

        response = self.client.get('/api/posts?author=harry')

        data =json.loads(response.data.decode()) 
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(data[0],
             {'id':1, 'text': 'post 1', 'author': 'harry'})


    def test_get_by_id_with_embed(self):
        self.db.purge_tables()
        self.client.post('/api/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')
        self.client.post('/api/comments',
            data='{\"text\": \"comment 1\", \"commentator\": \"peter\", "postId": 1 }')

        response = self.client.get('/api/posts/1/comments')

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
        self.client.post('/api/posts',
            data='{\"text\": \"post 1\", \"author\": \"harry\" }')
        self.client.post('/api/comments',
            data='{\"text\": \"comment 1\", \"commentator\": \"peter\", "postId": 1 }')

        response = self.client.get('/api/comments/1?expand=posts')

        data =json.loads(response.data.decode()) 
        sc = response.status_code

        self.assertEqual(sc, 200)
        self.assertEqual(data,
             { 'commentator': 'peter', 'id': 1, 'postId': 1, 'text': 'comment 1',
               'post': {'id':1, 'text': 'post 1', 'author': 'harry'}
             })



if __name__ == "__main__":
    unittest.main()