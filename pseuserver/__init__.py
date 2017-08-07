"""
PseuServer is a zero-coding, restful fake api web server for developers.

PseuServer provides most common GET, POST, PUT, DELETE methods with a configurable
backend. It has support for handy querying as well.

.. codeauthor:: Harry Ho <harry.ho_long@yahoo.com>

Usage example:

- Create a file *config.json* as following sample

{
    "db": "db.json",
    "routes":[
        "/posts",
        "/comments"
    ]
}

- Install the server

$ pip install pseuserver

- Launch the server

$ python pseuserver



"""

from flask import Flask
from flask import abort, request, make_response, current_app , Response

from pprint import pprint as pp
from pseuserver.methods import *
import json
# from json import dumps
import sys
import os
import ntpath

from functools import wraps, partial
import re
import operator
# from collections import Mapping
from pseuserver.settings import *



class PseuServer(object):    
    """" PseuServer is the restful API for python developers """

    def __init__(self, app=None, cfg_file = '', prefix='' ):

        self.this_directory = os.path.dirname(os.path.realpath(__file__))
        self.urls = {}
        self.routes = []
        self.prefix = prefix or DEFAULT_API_PREFIX
        self.default_mediatype = DEFAULT_MEDIATYPE
        self.app = None
        self.config_file = cfg_file or DEFAULT_CONFIG
        self.db_file = None
        self.db = DEFAULT_DB

        if app is not None:
            self.app = app
            self.load_config()
            self.add_routes()

            print('\n \(^_^)/ Hi \n')
            print('Loading %s is done. \n' % ntpath.basename(self.config_file))

            if len(self.urls) > 0:
                print('Resource : ')

            for url in self.urls:
                print(' %s%s ' % ( self.prefix, url))

            print('\nDatabase: %s \n' % self.db)



    def _complete_routes(self, url_part):
        """This method is used to defer the construction of the final url
        :param url_part: The part of the url is registered with prefix and route.
        :param url_part: string
        """
        basic_routes = ['', '/', '/<int:id>', '/<int:id>/<string:embed>']

        for i in range(len(basic_routes)):
            basic_routes[i] = '%s%s%s' % ( self.prefix , url_part , basic_routes[i])

        return basic_routes 


    def load_config(self):
        if os.path.exists(self.config_file):
            self.this_directory = os.path.dirname(self.config_file)
        else:
            self.config_file = os.path.join(os.getcwd(), self.config_file) 

            if os.path.exists(self.config_file):
                self.this_directory = os.path.dirname(self.config_file)
            else:                
                raise ValueError('The %s is not found.' % DEFAULT_CONFIG)       
            
        
        with open(self.config_file) as cfg:
            data = json.load(cfg)
            if data:
                try:
                    self.urls = data[CONFIG_ROUTES]
                    self.prefix = data[CONFIG_PREFIX] if CONFIG_PREFIX in data else self.prefix
                    self.db = data[CONFIG_DB] if CONFIG_DB in data else DEFAULT_DB
                    self.db_file = os.path.join(self.this_directory, self.db)
                except ValueError as e:
                    raise ValueError('The routes is missing in the %s file. '% self.config_file )
            else:
                raise ValueError('The config.json file should not be empty.')
        
    
    def add_routes(self, **kwargs):
        """ Add routes to support HTTP methods: GET, POST, PUT, DELETE """
        rest_api = server_api(self.prefix, self.urls, self.db_file)
        for url in self.urls:
            rules = self._complete_routes(url)
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

