from flask import Flask
from flask import abort, request, make_response, current_app , Response

from pprint import pprint as pp
from flatapi.methods import *
import json
# from json import dumps
import sys
import os
import ntpath

from functools import wraps, partial
import re
import operator
# from collections import Mapping
from flatapi.settings import *



class FlatApi(object):    
    """" FlatApi is the restful API for python developers """

    def __init__(self, app=None, cfg_file = '', prefix='', storage='' ):
        """
        This method is used to initialize FlatApi instance
        :param app: The instance of Flask
        :type app: Flask
        :param cfg_file: The api config json file. The default is config.json
        :type cfg_file: string
        :param prefix: The prefix of api 
        :type prefix: string   
        :param storage: The option of storage : FILE | MEMORY. If the storage is MEMORY,
                        the built-in cache with MemoryStorage will be instaniated ingoring
                        the cfg_file. 
        :type storage: string                   
        """
        self.this_directory = os.path.dirname(os.path.realpath(__file__))
        self.urls = {}
        self.routes = []
        self.prefix = prefix or DEFAULT_API_PREFIX
        self.default_mediatype = DEFAULT_MEDIATYPE
        self.app = None
        self.config_file = cfg_file # or  DEFAULT_CONFIG if not no_cfg else None
        self.db_file = None
        self.db = DEFAULT_DB
        self.storage = storage
        self.cache = CachingMiddleware(MemoryStorage)() if storage == MEMORY_STORAGE else None

        if self.prefix and not self.prefix.startswith('/'):
            self.prefix =  '/' + self.prefix
            
        if app is not None:
            self.app = app
            self.load_config()
            self.add_routes()


            print('\n \(^_^)/ Hi \n')
            print('Loading %s is done. \n' % (ntpath.basename(self.config_file) if self.config_file else '') )
            if not self.config_file:
                print('There is no config file found. FlatApi starts with built-in configuration.\n')

            if len(self.urls) > 0:
                print('Resource : ')
            else:
                print('Resource : ')
                print('%s/<string:doc> -- The doc is the collection name\n \
                    you want to post or put the object. '% (self.prefix))
                print('%s/<string:doc>/<int:id> --The id is the unique id for query or delete. '% (self.prefix))

            for url in self.urls:
                print(' %s%s ' % ( self.prefix, url))
            
            

            if self.storage == FILE_STORAGE:
                print('\nDatabase: %s \n' % self.db)
            else:
                print('\nDatabase: Memory  \n')



    def complete_routes(self, url_part):
        """This method is used to defer the construction of the final url
        :param url_part: The part of the url is registered with prefix and route.
        :param url_part: string
        """
        basic_routes = ['', '/', '/<int:id>', '/<int:id>/<string:embed>']

        for i in range(len(basic_routes)):
            basic_routes[i] = '%s%s%s' % ( self.prefix , url_part , basic_routes[i])

        return basic_routes 


    def load_config(self):
        if self.config_file:
            if os.path.exists(self.config_file):
                self.this_directory = os.path.dirname(self.config_file)
            else:
                self.config_file = os.path.join(os.getcwd(), self.config_file) 

                if os.path.exists(self.config_file):
                    self.this_directory = os.path.dirname(self.config_file)

                    
                elif self.storage == FILE_STORAGE:                
                    raise ValueError('The %s is not found. Or use ' % DEFAULT_CONFIG)       
            
        if self.config_file and  os.path.exists(self.config_file):
            with open(self.config_file) as cfg:
                data = json.load(cfg)
                if data:
                    try:
                        self.urls = data[CONFIG_ROUTES]
                        self.prefix = data[CONFIG_PREFIX] if CONFIG_PREFIX in data else self.prefix
                        self.db = data[CONFIG_DB] if CONFIG_DB in data else DEFAULT_DB
                        self.db_file = os.path.join(self.this_directory, self.db)
                        self.storage = data[CONFIG_STORAGE] if CONFIG_STORAGE in data else FILE_STORAGE
                        self.cache = self.cache or (CachingMiddleware(MemoryStorage)() if self.storage \
                            and self.storage.upper() == MEMORY_STORAGE else None)

                        if self.prefix and not self.prefix.startswith('/'):
                            self.prefix =  '/' + self.prefix
                    except ValueError as e:
                        raise ValueError('The routes is missing in the %s file. '% self.config_file )
                else:
                    raise ValueError('The config.json file should not be empty.')
        
    
    def add_routes(self, **kwargs):
        """ Add routes to support HTTP methods: GET, POST, PUT, DELETE """
        rest_api = server_api(self.prefix, self.urls, self.db_file, self.storage, self.cache)

        # Always clean up old routes
        if len(self.routes) > 0:
            self.routes.clear()
            # self.app.

        for url in self.urls:
            rules = self.complete_routes(url)
            # pp(rules)

            for r in range(len(rules)):
                rule = rules[r]
                self.routes.append(rule)
                if r == 0: # e.g. /api/posts -> GET, POST
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'POST', 'DELETE'])
                if r == 1:  # e.g. /api/posts/ -> GET, POST
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'POST', 'DELETE'])
                elif r == 2: # e.g. /api/posts/1 -> GET, PUT, DELTETE
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'PUT', 'DELETE'])
                elif r == 3: # e.g. /api/posts/1/comments -> GET
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET'])
        

        if not self.config_file and not self.urls:  
            rules = self.complete_routes('/<string:doc>')
            for r in range(len(rules)):
                rule = rules[r]                
                if r == 0: # e.g. /api/posts -> GET, POST
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'POST', 'DELETE'])
                if r == 1:  # e.g. /api/posts/ -> GET, POST
                    self.routes.append(rule)
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'POST', 'DELETE'])
                elif r == 2: # e.g. /api/posts/1 -> GET, PUT, DELTETE
                    self.routes.append(rule)
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'PUT', 'DELETE'])
                elif r == 3: # e.g. /api/posts/1/comments -> GET
                    self.routes.append(rule)
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET'])    

