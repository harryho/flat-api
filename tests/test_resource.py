import unittest
from flask  import Flask
from flatapi import *
import flatapi
import requests
import json
from pprint import pprint as pp
import os
from flata import *



class TestResource(unittest.TestCase):
    def setUp(self):
        # flatapi.DEFAULT_CONFIG = 'test.config.json'
        _db = 'test.db.json'
        this_dir = os.path.dirname(os.path.realpath(__file__))
        
        self.db_file = os.path.join(this_dir, _db)
        self.db = Flata(self.db_file)



    def tearDown(self):
        self.db.close()

        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    

    def test_create(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)

        self.assertEqual( result ,
            {'id':1, 'text': 'post 1', 'author': 'harry'})

    def test_edit(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)

        self.assertEqual( result ,
            {'id':1, 'text': 'post 1', 'author': 'harry'})

        pp(kwargs)
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post updated\", \"author\": \"john\" }'
        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_QUERY][RESOURCE_ID] = 1

        result = edit(**kwargs)


        self.assertEqual( result[0] ,
            {'id':1, 'text': 'post updated', 'author': 'john'})

    def test_remove_all(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)
        
        self.assertEqual( result ,
            {'id':1, 'text': 'post 1', 'author': 'harry'})

        result = remove(**kwargs)

        assert len(self.db.table('posts').all()) == 0
        # self.assertEqual( result[0] , [1, 2])

    def test_remove_by_id(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)
        self.assertEqual( result ,
            {'id':1, 'text': 'post 1', 'author': 'harry'})

        result = create(**kwargs)

        self.assertEqual( result ,
            {'id':2, 'text': 'post 1', 'author': 'harry'})

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_QUERY][RESOURCE_ID] = 1
        result = remove(**kwargs)

        # assert len(self.db.all()) == 1
        self.assertEqual( result[0] , [1])

    def test_query_by_id(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_QUERY][RESOURCE_ID] = 1

        result = query(**kwargs)

        self.assertEqual( result ,
            {'id':1, 'text': 'post 1', 'author': 'harry'})
    

    def test_query_by_condition(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_QUERY]['author'] = 'harry'

        result = query(**kwargs)

        self.assertEqual( result[0] ,
            {'id':1, 'text': 'post 1', 'author': 'harry'})

    def test_query_with_embed(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)
        kwargs[RESOURCE_DOCUMENT] = 'comments'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"comment 1\", \"commentator\": \"peter\", "postId": 1 }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_QUERY][RESOURCE_ID] = 1
        kwargs[RESOURCE_QUERY][RESOURCE_EMBED] = 'comments'

        result = query(**kwargs)

        self.assertEqual( result ,
            {'id':1, 'text': 'post 1', 'author': 'harry',
                'comments': [{'commentator': 'peter',
               'id': 1,
               'postId': 1,
               'text': 'comment 1'}]
             })

    def test_query_with_expand(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)
        kwargs[RESOURCE_DOCUMENT] = 'comments'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"comment 1\", \"commentator\": \"peter\", "postId": 1 }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_DOCUMENT] = 'comments'
        kwargs[RESOURCE_QUERY][RESOURCE_ID] = 1
        kwargs[RESOURCE_QUERY][RESOURCE_EXPAND] = 'posts'

        result = query(**kwargs)

        self.assertEqual( result ,
            { 'commentator': 'peter', 'id': 1, 'postId': 1, 'text': 'comment 1',
               'post': {'id':1, 'text': 'post 1', 'author': 'harry'}
             })


    def test_query_with_like(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\" }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_QUERY]['text_like'] = 'post'

        result = query(**kwargs)

        self.assertEqual( result[0] ,
            {'text': 'post 1', 'id': 1, 'author': 'harry'})

    def test_query_with_greater_than(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\", \"like\":8 }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_QUERY]['like_gt'] = 3

        result = query(**kwargs)

        self.assertEqual( result[0] ,
            {'text': 'post 1', 'id': 1, 'author': 'harry', "like":8})


    def test_query_with_greater_than_and_equal(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\", \"like\":8 }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_QUERY]['like_gte'] = 8

        result = query(**kwargs)

        self.assertEqual( result[0] ,
            {'text': 'post 1', 'id': 1, 'author': 'harry', "like":8})

    def test_query_with_less_than_and_equal(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\", \"like\":8 }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_QUERY]['like_lte'] = 8

        result = query(**kwargs)

        self.assertEqual( result[0] ,
            {'text': 'post 1', 'id': 1, 'author': 'harry', "like":8})

    def test_query_with_less_than(self):
        self.db.purge_tables()
        kwargs = {}
        kwargs[CONFIG_DB] = self.db_file
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_DATA] = b'{\"text\": \"post 1\", \"author\": \"harry\", \"like\":8 }'

        result = create(**kwargs)

        kwargs[RESOURCE_QUERY] = {}
        kwargs[RESOURCE_DOCUMENT] = 'posts'
        kwargs[RESOURCE_QUERY]['like_lt'] = 80

        result = query(**kwargs)

        self.assertEqual( result[0] ,
            {'text': 'post 1', 'id': 1, 'author': 'harry', "like":8})

if __name__ == "__main__":
    unittest.main()            